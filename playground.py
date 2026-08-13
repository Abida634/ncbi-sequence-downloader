from downloader.validator import is_non_empty
from downloader.exceptions import DownloaderError

print(is_non_empty("NM_001301717"))   # Should print: True
print(is_non_empty("   "))            # Should print: False
print(DownloaderError)                # Should print the class reference
