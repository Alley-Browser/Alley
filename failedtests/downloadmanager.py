import unittest
from src.DownloadManager import DownloadDialog

class TestDownloadDialog(unittest.TestCase):

    def test_filename(self):
        dialog = DownloadDialog('url', 'file.zip')
        self.assertEqual(dialog.filename, 'file.zip')

    def test_download_progress(self):
        dialog = DownloadDialog('url', 'file.zip')
        dialog.download_progress(512, 1024)
        self.assertEqual(dialog.bytes_received, 512)
        self.assertEqual(dialog.bytes_total, 1024)

    def test_download_finished(self):
        dialog = DownloadDialog('url', 'file.zip')
        dialog.download_finished()
        self.assertTrue(dialog.file.closed)

    def test_delete_download(self):
        dialog = DownloadDialog('url', 'file.zip')
        dialog.delete_download()
        self.assertTrue(dialog.downloads == [])

    def test_start_download(self):
        dialog = DownloadDialog('url', 'file.zip')
        dialog.start_download()
        self.assertIsNotNone(dialog.networkManager)
        self.assertIsNotNone(dialog.reply)

    def test_delete_all_downloads(self):
        dialog = DownloadDialog('url', 'file.zip')
        dialog.delete_all_downloads()
        self.assertTrue(dialog.downloads == [])

if __name__ == '__main__':
    unittest.main()
