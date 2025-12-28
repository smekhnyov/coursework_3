import ssl

from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql
from config import *
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/table', methods=['GET'])
def get_tables():
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = [table[0] for table in cur.fetchall()]
    return jsonify(tables)


@app.route('/column/<table>', methods=['GET'])
def get_columns(table):
    cur = conn.cursor()
    cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
    columns = [column[0] for column in cur.fetchall()]
    return jsonify(columns)

@app.route('/column_types/<table>', methods=['GET'])
def get_column_types(table):
    try:
        cur = conn.cursor()
        query = """
            SELECT 
                c.column_name, 
                c.data_type, 
                c.is_nullable, 
                c.column_default,
                c.character_maximum_length,
                (SELECT 
                    json_agg(row_to_json(fk)) 
                FROM (
                    SELECT 
                        kcu.column_name AS fk_column,
                        ccu.table_name AS fk_table,
                        ccu.column_name AS fk_table_column
                    FROM 
                        information_schema.table_constraints AS tc 
                        JOIN information_schema.key_column_usage AS kcu
                          ON tc.constraint_name = kcu.constraint_name
                        JOIN information_schema.constraint_column_usage AS ccu
                          ON ccu.constraint_name = tc.constraint_name
                    WHERE 
                        constraint_type = 'FOREIGN KEY' AND 
                        tc.table_name = %s AND 
                        kcu.column_name = c.column_name
                ) AS fk) AS foreign_keys
            FROM information_schema.columns AS c
            WHERE c.table_name = %s
            ORDER BY c.ordinal_position;
        """
        cur.execute(query, (table, table))
        rows = cur.fetchall()
        columns = []
        for row in rows:
            column = {
                'name': row[0],
                'type': row[1],
                'is_nullable': row[2],
                'default': row[3],
                'max_length': row[4],
                'foreign_keys': row[5]
            }
            if column['foreign_keys']:
                fk = column['foreign_keys'][0]
                fk_query = sql.SQL("SELECT {fk_column} FROM {fk_table}").format(
                    fk_column=sql.Identifier(fk['fk_table_column']),
                    fk_table=sql.Identifier(fk['fk_table'])
                )
                cur.execute(fk_query)
                column['options'] = [{'value': row[0], 'label': row[0]} for row in cur.fetchall()]
            columns.append(column)
        cur.close()
        return jsonify({'status': 'success', 'columns': columns}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/primary_keys/<table>', methods=['GET'])
def get_primary_key_values(table):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
            WHERE tc.table_name = %s AND tc.constraint_type = 'PRIMARY KEY'
        """, (table,))
        primary_key_column = cur.fetchone()
        if not primary_key_column:
            return jsonify({'status': 'error', 'message': 'Первичный ключ не найден'}), 400

        primary_key_column = primary_key_column[0]

        cur.execute(f"SELECT DISTINCT {primary_key_column} FROM {table}")
        rows = cur.fetchall()
        primary_key_values = [row[0] for row in rows]
        cur.close()
        return jsonify({'status': 'success', 'primary_key_values': primary_key_values}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/data/<table>/<column>', methods=['GET'])
def get_data(table, column):
    cur = conn.cursor()
    if column != "all":
        cur.execute(f"SELECT {column} FROM {table}")
    else:
        cur.execute(f"SELECT * FROM {table}")
    colnames = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    return jsonify({"columns": colnames, "rows": rows})

@app.route('/data/<table>', methods=['GET'])
def get_data_by_id(table):
    id = request.args.get('id')
    if not id:
        return jsonify({'status': 'error', 'message': 'ID не указан'}), 400

    try:
        cur = conn.cursor()
        cur.execute(f"""
            SELECT kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
            WHERE tc.table_name = %s AND tc.constraint_type = 'PRIMARY KEY'
        """, (table,))
        primary_key = cur.fetchone()[0]

        query = sql.SQL("SELECT * FROM {table} WHERE {primary_key} = %s").format(
            table=sql.Identifier(table),
            primary_key=sql.Identifier(primary_key)
        )
        cur.execute(query, (id,))
        colnames = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        cur.close()
        return jsonify({"columns": colnames, "rows": rows})
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/insert', methods=['POST'])
def insert_data():
    data = request.get_json()
    table = data.get('table')
    insert_dict = data.get('data')

    if not table:
        return jsonify({'status': 'error', 'message': 'Название таблицы отсутствует'}), 400

    if not isinstance(insert_dict, dict):
        return jsonify({'status': 'error', 'message': 'Данные должны быть в виде словаря'}), 400

    if not insert_dict:
        return jsonify({'status': 'error', 'message': 'Словарь данных пуст'}), 400

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                column_name, 
                column_default
            FROM information_schema.columns
            WHERE table_name = %s
        """, (table,))
        columns_info = cur.fetchall()

        columns_to_insert = []
        values_to_insert = []
        for column, default in columns_info:
            if default and 'nextval' in default:
                continue
            elif column in insert_dict:
                value = insert_dict[column]
                columns_to_insert.append(column)
                values_to_insert.append(value)

        if not columns_to_insert:
            return jsonify({'status': 'error', 'message': 'Нет данных для вставки'}), 400

        query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table),
            sql.SQL(', ').join(map(sql.Identifier, columns_to_insert)),
            sql.SQL(', ').join(sql.Placeholder() for _ in columns_to_insert)
        )

        cur.execute(query, values_to_insert)
        conn.commit()
        cur.close()
        return jsonify({'status': 'success', 'message': 'Данные успешно добавлены'}), 200

    except Exception as e:
        conn.rollback()
        error_message = str(e)
        return jsonify({'status': 'error', 'message': f'Ошибка при добавлении данных: {error_message}'}), 500

@app.route('/update', methods=['POST'])
def update_data():
    data = request.get_json()
    table = data.get('table')
    update_dict = data.get('data')
    condition = data.get('condition')

    if not table:
        return jsonify({'status': 'error', 'message': 'Table не указан'}), 400

    if not isinstance(update_dict, dict):
        return jsonify({'status': 'error', 'message': 'Данные должны быть в виде словаря'}), 400

    if not update_dict:
        return jsonify({'status': 'error', 'message': 'Словарь данных пуст'}), 400

    if not condition:
        return jsonify({'status': 'error', 'message': 'Условие обновления не указано'}), 400

    try:
        cur = conn.cursor()

        cur.execute(f"""
            SELECT kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
            WHERE tc.table_name = %s AND tc.constraint_type = 'PRIMARY KEY'
        """, (table,))
        primary_key = cur.fetchone()[0]

        set_clause = ', '.join([f"{key} = %s" for key in update_dict.keys()])
        query = sql.SQL("UPDATE {table} SET {set_clause} WHERE {primary_key} = %s").format(
            table=sql.Identifier(table),
            set_clause=sql.SQL(set_clause),
            primary_key=sql.Identifier(primary_key)
        )
        values = list(update_dict.values()) + [condition]

        cur.execute(query, values)
        conn.commit()
        cur.close()
        return jsonify({'status': 'success', 'message': 'Данные успешно обновлены'}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
@app.route('/delete', methods=['DELETE'])
def delete_data():
    data = request.get_json()
    table = data.get('table')
    key_value = data.get('key_value')

    if not table:
        return jsonify({'status': 'error', 'message': 'Название таблицы отсутствует'}), 400

    if not key_value:
        return jsonify({'status': 'error', 'message': 'Значение первичного ключа отсутствует'}), 400

    try:
        cur = conn.cursor()

        cur.execute(f"""
            SELECT kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
            WHERE tc.table_name = %s AND tc.constraint_type = 'PRIMARY KEY'
        """, (table,))
        primary_key = cur.fetchone()
        if not primary_key:
            return jsonify({'status': 'error', 'message': 'Первичный ключ не найден'}), 400

        primary_key = primary_key[0]

        query = sql.SQL("DELETE FROM {table} WHERE {primary_key} = %s").format(
            table=sql.Identifier(table),
            primary_key=sql.Identifier(primary_key)
        )
        cur.execute(query, (key_value,))
        conn.commit()
        cur.close()
        return jsonify({'status': 'success', 'message': 'Запись успешно удалена'}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/custom', methods=['POST'])
def execute_custom_command():
    data = request.get_json()
    command = data.get('command')

    if not command:
        return jsonify({'status': 'error', 'message': 'Команда не указана'}), 400

    try:
        cur = conn.cursor()
        cur.execute(command)
        if cur.description:
            rows = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
            result = {'columns': colnames, 'rows': rows}
        else:
            conn.commit()
            result = {'message': 'Команда выполнена успешно'}
        cur.close()
        return jsonify({'status': 'success', 'result': result}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

