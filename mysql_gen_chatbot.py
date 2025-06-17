import pymysql
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

Client = OpenAI()

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "8910",
    "database": "OpenAi", 
    "port": 3306,
    "cursorclass": pymysql.cursors.Cursor  
}

def get_schema_and_relationships():
    print("Attempting to connect...")
    try:
        conn = pymysql.connect(**MYSQL_CONFIG)
        print("Successfully connected to the database")
    except Exception as e:
        print("Error while connecting to MySQL:", e)
        return None, None

    with conn.cursor() as cursor:
        # Get tables
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = %s;
        """, (MYSQL_CONFIG["database"],))
        tables = [row[0] for row in cursor.fetchall()]

        schema_lines = []
        relationship_lines = []

        for table in tables:
            cursor.execute("""
                SELECT column_name, column_type
                FROM information_schema.columns
                WHERE table_schema = %s AND table_name = %s;
            """, (MYSQL_CONFIG["database"], table))
            columns = cursor.fetchall()
            col_text = ", ".join([f"{col} [{dtype}]" for col, dtype in columns])
            schema_lines.append(f"- {table}({col_text})")

            cursor.execute("""
                SELECT column_name, referenced_table_name, referenced_column_name
                FROM information_schema.key_column_usage
                WHERE table_schema = %s AND table_name = %s AND referenced_table_name IS NOT NULL;
            """, (MYSQL_CONFIG["database"], table))
            for col, ref_table, ref_col in cursor.fetchall():
                relationship_lines.append(f"- {table}.{col} → {ref_table}.{ref_col}")

    conn.close()

    return "\n".join(schema_lines), "\n".join(relationship_lines)


PROMPT_TEMPLATE = """
You are an SQL assistant. Based on the schema below, write SQL to answer the user's question.

Tables:
{tables}

Relationships:
{relationships}

Instructions:
- Use INNER JOIN when you need only matching records from both tables.
- Use LEFT JOIN when you want all records from the first (left) table even if there's no match on the right table.
- Use RIGHT JOIN when you want all records from the right table even if there's no match on the left table.
- Decide the join type based on the question's wording and implied intent.

User Question:
"{question}"

Generate SQL:
"""


def generate_sql(user_question):
    tables_text, relationships_text = get_schema_and_relationships()
    if not tables_text:
        print("Could not retrieve schema.")
        return None

    prompt = PROMPT_TEMPLATE.format(
        tables=tables_text,
        relationships=relationships_text or "None",
        question=user_question
    )

    response = Client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful SQL assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    question = input("Ask your question: ")
    sql = generate_sql(question)
    if sql:
        print("\nGenerated SQL:\n", sql)
