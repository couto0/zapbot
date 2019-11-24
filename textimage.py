from PIL import Image, ImageFont, ImageDraw
from matplotlib import pyplot as plt


MAX_WIDTH = 500  # px
FONT_HEIGHT = 20
FONT = ImageFont.truetype("./fonts/LiberationSans-Bold.ttf",FONT_HEIGHT)

def break_lines(msg):

    words_list = msg.split(" ")
    font_size = FONT.getsize(msg)

    break_word = 0
    lines = list()
    temp = None
    for i in range(len(words_list)):
        temp = " ".join(words_list[break_word:i])

        if FONT.getsize(temp)[0] > 480: # Limit size
            phrase_break = " ".join(words_list[break_word:i-1])
            lines.append(phrase_break)
            break_word = i -1
            continue

    if temp != "":
        lines.append(temp)

    return lines

def make_image(img_path, msg, output_path):
    img = Image.open(img_path)

    perc = MAX_WIDTH / img.size[0]
    img_resized = img.resize((MAX_WIDTH, int(img.size[1] * perc)), Image.ANTIALIAS)


    lines = break_lines(msg) # Break multi
    total_height = (len(lines) * (FONT_HEIGHT + 5))+5
    text_img = Image.new("RGB", (MAX_WIDTH, total_height), color = (255,255,255))
    d = ImageDraw.Draw(text_img)
    origin = (10, 5)
    for i, phrase in enumerate(break_lines(msg)):
        d.text((origin[0], origin[1] + (i * (FONT_HEIGHT+4))), phrase, font=FONT, fill=(0,0,0))


    img_height = text_img.size[1] + img_resized.size[1]
    new_image = Image.new('RGB',(MAX_WIDTH, img_height), color=(255, 255, 255))

    new_image.paste(text_img, (0, 0))
    new_image.paste(img_resized,(0, text_img.size[1]))
    new_image.save(output_path)
    plt.imshow(new_image)
    plt.show()



    #plt.imshow(img_resized)
    #plt.show()


if __name__ == "__main__":
    phrase = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris ac bibendum turpis, nec pulvinar dolor. Suspendisse volutpat neque sit amet aliquam molestie. Praesent at elementum urna, a facilisis turpis. Nunc vel felis in purus consectetur ornare. Proin nisi leo, rhoncus. "*2
    phrase = "Usar o python e o pandas pra calcular calcular uns BI! "
    make_image("stonks.png", phrase, "teste.jpg")
