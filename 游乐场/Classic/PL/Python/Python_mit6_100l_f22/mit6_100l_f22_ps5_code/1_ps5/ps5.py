"""
# Problem Set 5
# Name:
# Collaborators:
"""

from PIL import Image, ImageFont, ImageDraw
import numpy


def make_matrix(color):
    """
    Generates a transformation matrix for the specified color.
    Inputs:
        color: string with exactly one of the following values:
               'red', 'blue', 'green', or 'none'
    Returns:
        matrix: a transformation matrix corresponding to
                deficiency in that color
    """
    # You do not need to understand exactly how this function works.
    if color == 'red':
        c = [[.567, .433, 0], [.558, .442, 0], [0, .242, .758]]
    elif color == 'green':
        c = [[0.625, 0.375, 0], [0.7, 0.3, 0], [0, 0.142, 0.858]]
    elif color == 'blue':
        c = [[.95, 0.05, 0], [0, 0.433, 0.567], [0, 0.475, .525]]
    elif color == 'none':
        c = [[1, 0., 0], [0, 1, 0.], [0, 0., 1]]
    return c


def matrix_multiply(m1, m2):
    """
    Multiplies the input matrices.
    Inputs:
        m1,m2: the input matrices
    Returns:
        result: matrix product of m1 and m2
        in a list of floats
    """

    product = numpy.matmul(m1, m2)
    if type(product) == numpy.int64:
        return float(product)
    else:
        result = list(product)
        return result


def img_to_pix(filename):
    """
    Takes a filename (must be inputted as a string
    with proper file attachment ex: .jpg, .png)
    and converts to a list of representing pixels.

    For RGB images, each pixel is a tuple containing (R,G,B) values.
    For BW images, each pixel is an integer.

    # Note: Don't worry about determining if an image is RGB or BW.
            The PIL library functions you use will return the 
            correct pixel values for either image mode.

    Returns the list of pixels.
    接收一个文件名（必须以字符串形式输入，并包含正确的文件扩展名，例如：.jpg, .png），并将其转换为表示像素的列表。

    对于RGB图像，每个像素是一个包含(R, G, B)值的元组。  
    对于黑白图像，每个像素是一个整数值。

    # 注意：无需担心判断图像是RGB还是黑白模式。  
            你所使用的PIL库函数将返回适用于任一图像模式的正确像素值。

    返回像素列表。

    Inputs:
        filename: string representing an image file, such as 'lenna.jpg'
        returns: list of pixel values 
                 in form (R,G,B) such as [(0,0,0),(255,255,255),(38,29,58)...] for RGB image
                 in form L such as [60,66,72...] for BW image
    """
    img = Image.open(filename)
    pixel_list = list(img.getdata())
    return pixel_list

def pix_to_img(pixels_list, size, mode):
    """
    Creates an Image object from a inputted set of RGB tuples.

    Inputs:
        pixels_list: a list of pixels such as the output of
                img_to_pixels.
        size: a tuple of (width,height) representing
              the dimensions of the desired image. Assume
              that size is a valid input such that
              size[0] * size[1] == len(pixels).
        mode: 'RGB' or 'L' to indicate an RGB image or a 
              BW image, respectively
    returns:
        img: Image object made from list of pixels
    从输入的RGB元组集合中创建一个图像对象。

    输入：
        pixels_list: 一个像素列表，例如img_to_pixels的输出。
        size: 一个表示所需图像尺寸的元组（宽度,高度）。假设size是有效输入，满足size[0] * size[1] == len(pixels)。
        mode: 'RGB' 或 'L'，分别表示RGB图像或黑白图像。

    返回：
        img: 由像素列表生成的图像对象。
    """
    img = Image.new(mode, size)
    img.putdata(pixels_list)
    return img


def filter(pixels_list, color):
    """
    pixels_list: a list of pixels in RGB form, such as
            [(0,0,0),(255,255,255),(38,29,58)...]
    color: 'red', 'blue', 'green', or 'none', must be a string representing 
           the color deficiency that is being simulated.
    returns: list of pixels in same format as earlier functions,
    transformed by matrix multiplication
    pixels_list: 一个以RGB形式表示的像素列表，例如
            [(0,0,0),(255,255,255),(38,29,58)...]
    color: 'red'、'blue'、'green' 或 'none'，必须是一个字符串，代表
           正在模拟的色觉缺陷类型。
    returns: 与之前函数相同格式的像素列表，
            通过矩阵乘法转换后的结果。
    """
    # 将浮点数列表转为整数列表
    float_array = numpy.array(matrix_multiply(pixels_list, make_matrix(color)))
    int_array = float_array.astype(int) 
    # # 将二维列表转换为元组列表
    # return [tuple(pixel) for pixel in int_array]
    pi_list = [tuple(pixel) for pixel in int_array]
    return pi_list 


##### PART 1 end

##### PART 2 start

def extract_end_bits(num_end_bits, pixel):
    """
    Extracts the last num_end_bits of each value of a given pixel.

    example for BW pixel:
        num_end_bits = 5
        pixel = 214

        214 in binary is 11010110. 
        The last 5 bits of 11010110 are 10110.
                              ^^^^^
        The integer representation of 10110 is 22, so we return 22.

    example for RBG pixel:
        num_end_bits = 2
        pixel = (214, 17, 8)

        last 3 bits of 214 = 110 --> 6
        last 3 bits of 17 = 001 --> 1
        last 3 bits of 8 = 000 --> 0

        so we return (6,1,0)

    Inputs:
        num_end_bits: the number of end bits to extract
        pixel: an integer between 0 and 255, or a tuple of RGB values between 0 and 255

    Returns:
        The num_end_bits of pixel, as an integer (BW) or tuple of integers (RGB).
    """
    t = 2**num_end_bits
    # 对于黑白图像的列表
    if type(pixel) == int:    
        return pixel % t
    # 对于彩色图像的列表元祖
    else:
        return (pixel[0] % t, pixel[1] % t, pixel[2] % t)


def reveal_bw_image(filename):
    """
    Extracts the single LSB for each pixel in the BW input image. 
    Inputs:
        filename: string, input BW file to be processed
    Returns:
        result: an Image object containing the hidden image
    """
    # 打开文件得到img对象数据
    op_img = Image.open(filename)
    pixel_list = list(op_img.getdata())
    # 提取黑白文件的最低有效位
    res_pix_list = [extract_end_bits(1, pix) for pix in pixel_list]
    # 将最低有效位的1与0转为差异更明显的数字255与0
    res_pix_list = [255 if e == 1 else 0 for e in res_pix_list]
    # 创建空img对象并填充
    res_img = Image.new("L", op_img.size)
    res_img.putdata(res_pix_list)
    return res_img

def reveal_color_image(filename):
    """
    Extracts the 3 LSBs for each pixel in the RGB input image. 
    Inputs:
        filename: string, input RGB file to be processed
    Returns:
        result: an Image object containing the hidden image
    """
    # 打开文件得到img对象数据
    op_img = Image.open(filename)
    pixel_list = list(op_img.getdata())
    # 提取彩色文件的3个最低有效位
    res_pix_list = [extract_end_bits(3, pixels) for pixels in pixel_list]
    # 3个最低有效位的范围为0～7，将值* (255/7),再转回整数元祖
    div_n = 255/7
    res_pix_list = [(int(pixs[0] * div_n), int(pixs[1] * div_n), int(pixs[2] * div_n)) 
                    for pixs in res_pix_list]
    # 创建空img对象并填充
    res_img = Image.new("RGB", op_img.size)
    res_img.putdata(res_pix_list)
    return res_img


def reveal_image(filename):
    """
    Extracts the single LSB (for a BW image) or the 3 LSBs (for a 
    color image) for each pixel in the input image. Hint: you can
    use a function to determine the mode of the input image (BW or
    RGB) and then use this mode to determine how to process the image.
    Inputs:
        filename: string, input BW or RGB file to be processed
    Returns:
        result: an Image object containing the hidden image
    """
    im = Image.open(filename)
    if im.mode == '1' or im.mode == 'L':
        return(reveal_bw_image(filename))
    elif im.mode == 'RGB':
        return(reveal_color_image(filename))
    else:
        raise Exception("Invalid mode %s" % im.mode)


def draw_kerb(filename, kerb):
    """
    Draws the text "kerb" onto the image located at "filename" and returns a PDF.
    Inputs:
        filename: string, input BW or RGB file
        kerb: string, your kerberos
    Output:
        Saves output image to "filename_kerb.xxx"
    """
    im = Image.open(filename)
    font = ImageFont.truetype("noto-sans-mono.ttf", 40)
    draw = ImageDraw.Draw(im)
    draw.text((0, 0), kerb, "white", font=font)
    idx = filename.find(".")
    new_filename = filename[:idx] + "_kerb" + filename[idx:]
    im.save(new_filename)
    return


def main():
    # Uncomment the following lines to test part 1

    # im = Image.open('image_15.png')
    # width, height = im.size
    # pixels = img_to_pix('image_15.png')

    # non_filtered_pixels = filter(pixels,'none')
    # im = pix_to_img(non_filtered_pixels, (width, height), 'RGB')
    # im.save("im.png")

    # red_filtered_pixels = filter(pixels,'red')
    # im2 = pix_to_img(red_filtered_pixels,(width,height), 'RGB')
    # im2.save("im2.png")

    # Uncomment the following lines to test part 2
    #
    print(extract_end_bits(1, 13)) # get one LSB -> return 1
    print(extract_end_bits(2, 13)) # get two LSBs -> return 1
    print(extract_end_bits(3, 13)) # get three LSBs -> return 5
    #
    im = reveal_image('hidden1.bmp')
    im.save("im_hidden1.png")

    im2 = reveal_image('hidden2.bmp')
    im2.save("im_hidden2.png")
    

if __name__ == '__main__':
    main()
