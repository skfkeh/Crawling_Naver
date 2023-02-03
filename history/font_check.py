import matplotlib.font_manager as fm

font_list = fm.findSystemFonts(fontpaths=None, fontext="ttf")
print(len(font_list))

f = [f.name for f in fm.fontManager.ttflist]
print(f)

for i in f:
    if i == "Malgun Gothic":
        print("맑은 고딕 있어요~")
    if i == "Apple SD Gothic Neo":
        print("맑은 고딕은 없지만, 애플 고딕은 있어요~")