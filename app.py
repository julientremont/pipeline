def main():
    """
    liste des query
    """
    sql_etudiant = """
    SELECT *
    FROM Etudiant
    """
    sql_enseignants = """
    SELECT [id]
      ,[Prenom]
      ,[Nom]
      ,[Num_classe]
      ,[Departement]
      ,[Tel]
      ,[email]
      ,[Annee_diplome]
    FROM [Ecole].[dbo].[Enseignants]
    """
    sql_etudiant_salle_enseignant = """
    SELECT et.[id] as id_etudiant
      ,et.[Prenom] as Prenom_etudiant
      ,et.[Nom] as Nom_etudiant
	  ,et.[Num_classe] 
	  ,en.[id] as id_enseignant
      ,en.[Prenom] as prenom_enseignant
      ,en.[Nom] as nom_enseignant
  FROM [Ecole].[dbo].[Etudiant] as et left join [Ecole].[dbo].[Enseignants] as en on et.[Num_classe] = en.[Num_classe]
  where en.[id] is not null
    """
    sql_etudiant_par_prof = """SELECT COUNT(*) as nombre_eleve,
    en.[Prenom],
    en.[Nom], 
    en.id
FROM [Ecole].[dbo].[Etudiant] as et left join [Ecole].[dbo].[Enseignants] as en on 
    et.[Num_classe] = en.[Num_classe]
GROUP BY en.[Prenom],en.[Nom], en.id
order by en.id
"""
    
    """
    Connects to a SQL database using pyodbc
    """
    import pyodbc
    import pandas as pd
    SERVER = 'NEU-PORT-103'
    DATABASE = 'Ecole'
    USERNAME = 'NEUILLY\j.tremont'
    PASSWORD = 'mp0117JUJU!'
    connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;TrustServerCertificate=yes'

    def curseur(query):
        conn = pyodbc.connect(connectionString)
        cursor = conn.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        nom_columns = []
        for desc in cursor.description:
            nom_columns.append(desc[0])
        result = []
        for row in records:
            row_dict = {}
            for id, value in enumerate(row):
                row_dict[nom_columns[id]] = value
            result.append(row_dict)
        result_tab = pd.DataFrame(result)
        cursor.close()
        conn.close()
        return result_tab
    """
    Print résultat
    """
    print("Pour chaque élève, sont enseignant lier par la classe")
    print("")
    print(curseur(sql_etudiant_salle_enseignant))
    print("")
    print("")
    print("Nb élève par enseignant")
    print("")
    print(curseur(sql_etudiant_par_prof))

if __name__ == "__main__":
    main()