# 读取excle
import xlrd as xlrd


def readuser_to_excle(file):
    """读取excle表中第二列准考证号"""
    myWorkbook = xlrd.open_workbook(file)

    mySheets = myWorkbook.sheets()  # 获取工作表list。

    mySheet = mySheets[0]  # 通过索引顺序获取。

    # 获取行数
    nrows = mySheet.nrows

    users = []
    for row in range(1,nrows):
        last_name = mySheet.cell_value(row, 0)
        sex = mySheet.cell_value(row, 1)
        if sex == "男":
            sex = 1
        else:
            sex = 2
        role = mySheet.cell_value(row, 2)
        if role == "学生":
            role = 3
        elif role == "老师":
            role = 2
        else:
            role = 1
        takeschoolyear = int(mySheet.cell_value(row, 3))
        status = mySheet.cell_value(row, 4)
        if status == "在读":
            status = 0
        elif status == "休学":
            status = 1
        elif status == "在职":
            status = 2
        else:
            status = 3

        livetime = mySheet.cell_value(row, 5)
        if livetime != "无期限":
            livetime = int(livetime[0])
        else:
            livetime = 0


        users.append({"last_name":last_name,"sex":sex,
                      "role":role,"takeschoolyear":takeschoolyear,"status":status,
                      "livetime":livetime})

    return users

