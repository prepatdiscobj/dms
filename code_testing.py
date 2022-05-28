import unittest
from file_copy_by_year import get_year, get_file_timestamp, access_all_files, copy_files_to_year


class MyTestCase(unittest.TestCase):
    def test_get_year(self):
        predicted_year = get_year(1471663579.0)
        expected_year = '2016'
        self.assertEqual(predicted_year, expected_year)  # add assertion here

    def test_get_file_timestamp(self):
        modified_time = get_file_timestamp('file_copy_by_year.py', "modified")
        accessed_time = get_file_timestamp('file_copy_by_year.py', "accessed")
        created_time = get_file_timestamp('file_copy_by_year.py', "created")
        mtime_year = get_year(modified_time)
        atime_year = get_year(accessed_time)
        ctime_year = get_year(created_time)
        self.assertEqual(mtime_year, '2022')
        self.assertEqual(atime_year, '2022')
        self.assertEqual(ctime_year, '2022')

    def test_access_all_files(self):
        all_files = list(access_all_files("C:\\Users\\signu\\Dropbox\\Projects\\dms"))
        python_files = [f for f in all_files if f.endswith('.py')]
        self.assertEqual(len(python_files), 2)

    def test_copy_files_to_year(self):
        count, failed = copy_files_to_year("C:\\Users\\signu\\Dropbox\\Projects\\dms", "C:\\Users\\signu\\test")
        self.assertEqual(count, 8)
        self.assertEqual(len(failed), 0)


if __name__ == '__main__':
    unittest.main()
