from DBConnection import DBConnection

conn = DBConnection()
conn.autocommit = True
cur = conn.getCursor()

# Fetch duplicate entry
cur.execute("""
SELECT [TEMP].[TargetID], [INV].[InventorID] FROM
(SELECT min([InventorID]) AS [TargetID], [Lname], [Mname], [Fname], [City], [State], [Country], [Rank]
FROM [NanoUSPTO].[dbo].[Inventors]
GROUP BY [Lname], [Mname], [Fname], [City], [State], [Country], [Rank]
HAVING count([InventorID]) > 1) AS TEMP
JOIN [NanoUSPTO].[dbo].[Inventors] AS [INV] 
ON [TEMP].[Lname] = [INV].[Lname]
AND [TEMP].[Mname] = [INV].[Mname]
AND [TEMP].[Fname] = [INV].[Fname]
AND [TEMP].[City] = [INV].[City]
AND [TEMP].[State] = [INV].[State]
AND [TEMP].[Country] = [INV].[Country]
AND [TEMP].[Rank] = [INV].[Rank]
""")

duplicate_rows = cur.fetchall()
duplicate_ids =  [x[1] for x in duplicate_rows if x[1] != x[0]]
replace_id = [(x[1], x[0]) for x in duplicate_rows if x[1] != x[0]]
# replace_id.append((410014, 410013))
# replace_id.append((448276, 448275))
# replace_id.append((419311, 419310))
# replace_id.append((430053, 430052))
# replace_id.append((412759, 412758))
# replace_id.append((412763, 412762))
# replace_id.append((462585, 462584))


# Update citation table
for pair in replace_id:
    sql = """
    UPDATE [NanoUSPTO].[dbo].[Invent]
    SET [InventorID] = {}
    WHERE [InventorID] = {}
    """.format(str(pair[1]), str(pair[0]))
    print("updating {}".format(str(pair[0])))
    cur.execute(sql)
    cur.commit()
print("Finished Update")

# remove the duplicate rows
for id in duplicate_ids:
    sql = """
    DELETE FROM [NanoUSPTO].[dbo].[Inventors]
    WHERE [InventorID] = {}
    """.format(str(id))
    print("deleting {}".format(str(id)))
    cur.execute(sql)
    cur.commit()
print("Finished delete")
# duplicate_ids = [x[0] for x in duplicate_rows]
# print(duplicate_ids)
cur.close()
conn.close()