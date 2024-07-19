def chuyen_doi_chu_cai_sang_so(chu_cai):
    """Chuyển đổi chữ cái sang số tương ứng trong Excel.
    
    Arguments:
    chu_cai : str : Chữ cái cần chuyển đổi
    
    Returns:
    int : Số tương ứng với chữ cái trong Excel
    """
    so_cot = 0
    for ky_tu in chu_cai:
        so_cot = so_cot * 26 + (ord(ky_tu.upper()) - 64)
    return so_cot

# Ví dụ sử dụng:
chu_cai = 'IA'
so_cot = chuyen_doi_chu_cai_sang_so(chu_cai)
print(f"Cột {chu_cai} tương ứng với cột thứ {so_cot-1} trong Pandas.")
