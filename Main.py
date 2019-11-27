# The entry point of the program which creates an instance of dbGAPFileProcessor
# which creates dbGAP analysis file processor threads
# which read the lines of analysis files
# # and inserts the SNPs with significance (p <= 0.0001)
# # into our PostgreSQL database table
# through the instance of DatabaseOperations class.
import dbGAPFileProcessor as dfp

if __name__ == '__main__':
    file_processor = dfp.dbGAPFileProcessor('/Users/gulsah/dbGAP/ftp.ncbi.nlm.nih.gov/dbgap/studies')
    file_processor.processDirectories()