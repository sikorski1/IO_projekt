import os
from PIL import Image
from ollama import Client

def generate_text(instruction, file_path):
    client = Client(
        host='http://192.168.0.186:11434'
    )
    result = client.generate(
        model='llava',  
        prompt=instruction,
        images=[file_path],
        stream=False
    )['response']
    return result.strip().lower()

def merge_images(image_paths, output_path):
    images = [Image.open(img_path) for img_path in image_paths]
    widths, heights = zip(*(img.size for img in images))

    total_width = max(widths)
    total_height = sum(heights)

    merged_image = Image.new('RGB', (total_width, total_height))

    y_offset = 0
    for img in images:
        merged_image.paste(img, (0, y_offset))
        y_offset += img.size[1]

    merged_image.save(output_path)

def main():
    instruction = "do we have here image which contains whiteboard? answer yes or no without any other information just one word"
    data_folder = './data'
    yes_images = []

    for filename in os.listdir(data_folder):
        if filename.endswith('.png'):
            print(filename)
            file_path = os.path.join(data_folder, filename)
            answer = generate_text(instruction, file_path)
            print(answer)
            if answer == 'yes':
                print("added")
                yes_images.append(file_path)

    if yes_images:
        merged_image_path = './merged_image.png'
        merge_images(yes_images, merged_image_path)
        final_instruction = "You will receive long image with whiteboard content. There should be multiple whiteboard in this image. Please generate notes for notes You receive from whiteboards!"
        notes = generate_text(final_instruction, merged_image_path)
        with open('./notes.txt', 'w') as notes_file:
            notes_file.write(notes)

if __name__ == "__main__":
    main()
