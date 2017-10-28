import dbGAPFileProcessor as dfp

if __name__ == '__main__':
    file_processor = dfp.dbGAPFileProcessor('/Users/gulsahsbg/Documents/phdThesis/dbGAP_wget/ftp.ncbi.nlm.nih.gov/dbgap/studies')
    file_processor.processDirectories()