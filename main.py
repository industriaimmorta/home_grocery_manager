from _hgm.hgm_main import HGManager

if __name__ == "__main__":
    HGM = HGManager()
    isolated = True
    HGM.run(isolated)

else:
    HGM = HGManager()
    isolated = False
    HGM.run(isolated)