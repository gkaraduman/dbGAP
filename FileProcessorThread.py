import threading
import pandas as pd

class FileProcessorThread(threading.Thread):
    def __init__(self, file_path, write_to_database, study_id):
        threading.Thread.__init__(self)
        self.file_path = file_path
        self.write_to_database = write_to_database
        self.study_id = study_id
        self.study_description = ''
        self.study_name = ''
        self.handled = False
        self.done = False
        self.containsSNPId = False

    def run(self):
        print("Starting file" + self.file_path)
        self.readFile(self.file_path)
        print("Exiting file " + self.file_path)

    def extractCommentLineCount(self, file_path):
        comment_line_count = 0
        analysisFile = open(file_path, 'r')
        for line in analysisFile:
            if (line.startswith('SNP ID') == False | line.startswith('ID	Analysis ID	SNP ID') == False):
                comment_line_count = comment_line_count + 1
                if (line.startswith('# SNP ID:')):
                    self.containsSNPId = True
                if (line.startswith('# Name:')):
                    comment, name = line.split("# Name:")
                    self.study_name = name.strip()
                if(line.startswith('# Description:')):
                    comment, description = line.split("# Description:")
                    self.study_description = description.strip()
            else:
                break

        return comment_line_count

    def readFile(self, file_path):
        row_count_to_skip = self.extractCommentLineCount(file_path)
        if(self.containsSNPId):
            analyses_rows = pd.read_table(file_path, sep="\t",
                                          skiprows=row_count_to_skip,
                                              index_col=False);
            significant_rows = analyses_rows.loc[analyses_rows['P-value'] <= 0.001]
            significant_rows = significant_rows.drop_duplicates(subset=['SNP ID', 'P-value'])
            significant_rows = significant_rows[['SNP ID', 'P-value']]

            for index, row in significant_rows.iterrows():
                query_str = 'INSERT INTO dbgap_0_001 values (%s, %s, %s, %s, %s)'
                query_params = (row.get(0), row.get(1), self.study_id, self.study_name, self.study_description)
                self.write_to_database.executeQuery(query_str, query_params)
                self.write_to_database.commit()

        self.done = True