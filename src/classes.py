import pytesseract

class Slide:
    """slide object, contains name text and word count
    """
    def __init__(self, slide, name):
        self.name = name
        self.get_text(slide)
        self.word_count = len(self.text.split())
        
    def __repr__(self):
        return "slide(name text word_count)"

    def __str__(self):
        return "slide: {} {}".format(self.name, self.word_count)

    def get_text(self,slide):
        """gets the text from the slide

        Args:
           self.slide: slide image

        Returns:
            the text of the slide

        """
        text = pytesseract.image_to_string(slide)
        self.text = text


class Student:
    """student object contains face coordinants, name, attention points
    """
    def __init__(self, face, name):
        self.face = face
        self.name = name
        self.box = face['box']
        self.face_points = face['keypoints']
        self.attention_points = (0,0)
        self.reference_points = (0,0)
        self.attention_angle_list = []
        self.mode_attention_angle = 0
        self.attention_angle_per_frame = []
        self.absent_from_frame = 0
        self.present_in_frame = 0
        
    @property
    def update_face(self):
       self.face = face
       self.box = face['box']
       self.face_points = face['keypoints']

    @update_face.setter
    def update_face(self, face):
        self.face = face
        self.box = face['box']
        self.face_points = face['keypoints']
        
    def __repr__(self):
        return "student('{}', '{}')".format(self.box, self.name)

    def __str__(self):
        return "student: {} attentiveness: {}".format(self.name, self.attention_angle_list)
