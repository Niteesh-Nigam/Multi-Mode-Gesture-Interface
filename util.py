import cv2
import numpy as np

# Function to create a keyboard layout
# def create_keyboard_layout(img_size_x, img_size_y):
def create_keyboard_layout(rect_x1, rect_x2, rect_y1, rect_y2):
    img_size_x = rect_x2-rect_x1
    img_size_y= rect_y2-rect_y1
    img = np.zeros((img_size_y, img_size_x, 3), dtype=np.uint8)
    keys = [
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]
    ]
    key_width = int(img_size_x / 11)
    key_spaces = int(key_width / 8)
    num_rows_keys = len(keys)
    num_columns_keys = len(keys[0])

    class Button:
        def __init__(self, pos, text, size=(key_width, key_width)):
            self.pos = pos
            self.text = text
            self.size = size

    button_list = []
    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            x = int((j * key_width) + (j * key_spaces))
            y = int((i * key_width) + (i * key_spaces))
            button_list.append(Button([x, y], key))

    # Draw all buttons
    for button in button_list:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, (x, y), (x + button.size[0], y + button.size[1]), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + int(key_width / 6), y + int(key_width / 1.2)),
                    cv2.FONT_HERSHEY_PLAIN, key_width / 17, (255, 255, 255), key_width // 15)

        index_text_start = (num_rows_keys - 1) * num_columns_keys  # For the first key in the last row
        text_start_x = button_list[index_text_start].pos[0]
        text_start_y = button_list[index_text_start].pos[1] + key_width + key_spaces

        index_end_text = (num_rows_keys * num_columns_keys) - 1
        text_end_x = button_list[index_end_text].pos[0] - key_spaces
        text_end_y = button_list[index_end_text].pos[1] + key_width * 2

        cv2.rectangle(img, (text_start_x, text_start_y), (text_end_x, text_end_y), (175, 0, 175), cv2.FILLED)



    return img, button_list, text_start_x, text_start_y, text_end_x, text_end_y, key_width

def map_to_cropped_frame(hand_x, hand_y, frame_width, frame_height, crop_width, crop_height):
    # Calculate crop margins
    margin_x = (frame_width - crop_width) // 2
    margin_y = (frame_height - crop_height) // 2

    # Map coordinates from full frame to cropped frame
    cropped_x = hand_x - margin_x
    cropped_y = hand_y - margin_y

    # Ensure the coordinates are within the cropped frame boundaries
    cropped_x = max(0, min(crop_width, cropped_x))
    cropped_y = max(0, min(crop_height, cropped_y))

    return cropped_x, cropped_y

# Example usage
# if __name__ == "__main__":
#     img = create_keyboard_layout()
#     cv2.imshow('Keyboard Layout', img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
