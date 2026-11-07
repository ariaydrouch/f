import fitz,sys
doc=fitz.open("HiLabs_Case_Deck_Case_Management_Workbench.pdf")
for i,p in enumerate(doc):
    p.get_pixmap(dpi=110).save(f"/tmp/v4_{i+1}.png")
print(len(doc))
