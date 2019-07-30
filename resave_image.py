import os
import traceback

from PIL import Image

from utils import Inputs
from utils import searchFile


def main():
    # 提示用户输入
    print("该程序用于检索指定目录（包括子目录）下的所有.jpg图片，将它们另存到当前目录。")
    Inputs.path = Inputs.input_path("请输入要检索的目录：")
    # Inputs.suffix = ".jpg"

    print("检索所有图片...")
    file_list = searchFile(Inputs.path, ".jpg")+searchFile(Inputs.path,
                                                           ".jpeg")+searchFile(Inputs.path, ".png")

    # 创建一个保存被修改图片的文件夹
    result_dir = os.path.join(os.getcwd(), "resaved_images")
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)

    print("开始修改...")
    for path in file_list:
        try:
            img = Image.open(path)

            # 可能有些图片只是后缀名为jpg，实际上却不是RGB模式，这里把它们都转换成RGB模式
            if img.mode != "RGB":
                img = img.convert("RGB")

            # 创建保存图片的子目录
            result_path = path.replace(Inputs.path, result_dir, 1)
            result_path = result_path[:result_path.rfind('.')]+".jpg"     # 保存为.jpg文件
            os.makedirs(os.path.dirname(result_path), exist_ok=True)

            # 保存图片
            img.save(result_path, quality=100)
            print("已保存：{}".format(result_path))

        except:
            print("处理失败：{}".format(path))
            traceback.print_exc()

    print("\n已全部完成。\n")
    return 0


if __name__ == "__main__":
    try:
        main()
    except:
        print("\n运行出错！\n")
        traceback.print_exc()
    finally:
        os.system("pause")
