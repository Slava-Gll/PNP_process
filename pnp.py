from pnpproc import PnpConverter
pnp = PnpConverter('/test_ready')
pnp.update_folder()
print(pnp.convert(r"C:\Users\SLG\Desktop\py\PNP\Cucumber_utf8.txt"))
print(pnp.last_error)