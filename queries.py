insert_cities_command = f'INSERT INTO cities (ref, title) VALUES (%s, %s);'

insert_products_command = f'INSERT INTO products (ref, title) VALUES (%s, %s);'

insert_branches_command = f'INSERT INTO branches (ref, title, ref_city, short_name, region) \
        VALUES (%s, %s, %s, %s, %s);'

insert_sales_command = f'INSERT INTO sales (datetime, ref_branch, ref_product, quantity, price) \
        VALUES (%s, %s, %s, %s, %s);'

insert_products_with_category_command = 'INSERT INTO products_with_category (title, category) VALUES (%s, %s);'


create_products_with_category_table = """CREATE TABLE IF NOT EXISTS products_with_category (
                                                id SERIAL PRIMARY KEY,
                                                title TEXT,
                                                category VARCHAR(50)
                                        );"""

                                        
create_tables_commands = [
    (
        """CREATE TABLE IF NOT EXISTS cities (
                    id SERIAL PRIMARY KEY,
                    ref UUID UNIQUE,
                    title VARCHAR(100)
        );""", ()
    ),
    (
        """CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY,
                    ref UUID UNIQUE,
                    title TEXT
        );""", ()
    ),
    (
        """CREATE TABLE IF NOT EXISTS branches (
                    id SERIAL PRIMARY KEY,
                    ref UUID UNIQUE, 
                    title TEXT,
                    ref_city UUID REFERENCES cities(ref),
                    short_name VARCHAR(50),
                    region VARCHAR(50)
        );""", ()
    ),
    (
        """CREATE TABLE IF NOT EXISTS sales (
                    id SERIAL PRIMARY KEY,
                    datetime TIMESTAMP,
                    ref_branch UUID REFERENCES branches (ref),
                    ref_product UUID REFERENCES products (ref),
                    quantity NUMERIC,
                    price NUMERIC
        );""", ()
    )
]

set_indexes = [
    (
        'CREATE INDEX IF NOT EXISTS idx_products ON products (ref);', ()
    ),
    (
        'CREATE INDEX IF NOT EXISTS idx_sales_ref_branch ON sales (ref_branch);', ()
    ),
    (
        'CREATE INDEX IF NOT EXISTS idx_sales_ref_product ON sales (ref_product);', ()
    )
]


top_10_shops = """SELECT title, count FROM
                    (SELECT ref_branch, COUNT(*) FROM sales 
                    	LEFT JOIN branches ON sales.ref_branch=branches.ref
                    	WHERE title NOT LIKE '%клад%'
                    	GROUP BY ref_branch
                    	ORDER BY count DESC
                    	LIMIT 10) AS top_10_branches
                    		LEFT JOIN branches ON top_10_branches.ref_branch=branches.ref
                    		ORDER BY count DESC;"""

top_10_storages = """SELECT title, count FROM
                        (SELECT ref_branch, COUNT(*) FROM sales 
                        	LEFT JOIN branches ON sales.ref_branch=branches.ref
                        	WHERE title LIKE '%клад%'
                        	GROUP BY ref_branch
                        	ORDER BY count DESC
                        	LIMIT 10) AS top_10_branches
                        		LEFT JOIN branches ON top_10_branches.ref_branch=branches.ref
                        		ORDER BY count DESC;"""

top_10_products_among_storages = """SELECT title, count FROM
                                    	(SELECT ref_product, COUNT(*) FROM sales 
                                    	LEFT JOIN branches ON sales.ref_branch=branches.ref 
                                    	WHERE title LIKE '%клад%'
                                    	GROUP BY ref_product
                                    	ORDER BY count DESC
                                    	LIMIT 10) AS top_10_products
                                    		LEFT JOIN products ON top_10_products.ref_product=products.ref;"""

top_10_products_among_shops = """SELECT title, count FROM
	                                (SELECT ref_product, COUNT(*) FROM sales 
	                                LEFT JOIN branches ON sales.ref_branch=branches.ref 
	                                WHERE title NOT LIKE '%клад%'
	                                GROUP BY ref_product
	                                ORDER BY count DESC
	                                LIMIT 10) AS top_10_products
	                                	LEFT JOIN products ON top_10_products.ref_product=products.ref;"""

top_10_most_selling_cities = """SELECT cities.title, COUNT(*) FROM sales 
	                                LEFT JOIN branches ON sales.ref_branch=branches.ref
	                                LEFT JOIN cities ON branches.ref_city=cities.ref
	                                GROUP BY cities.title
	                                ORDER BY count DESC
	                                LIMIT 10;"""

sales_of_products = """SELECT title, count FROM 
	                        (SELECT ref_product, COUNT(*) FROM sales
	                        GROUP BY ref_product) AS sales_of_products
	 	                        LEFT JOIN products ON sales_of_products.ref_product=products.ref;"""