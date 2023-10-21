"""
This script could be used to test Pololu img moving in pygame.
"""

import sys
import os
import pygame
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer, QRectF
script_dir = os.path.dirname(os.path.abspath(__file__))
pictures_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pictures"
)

class PygameGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Change the resolution to your desired size
        screen = pygame.display.set_mode((800, 600))

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.Surface((400, 400))
        self.clock = pygame.time.Clock()

        # Load image
        self.img = pygame.image.load(os.path.join(pictures_dir, "pololu_img.png")).convert()
        self.img_rect = self.img.get_rect(center=self.screen.get_rect().center)
        self.degree = 0

        # Create QTimer for updating the display
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)
        self.timer.start(16)  # Refresh every 16 milliseconds (~60 FPS)

    def update_display(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                QApplication.quit()

        # Rotate image
        rot_img = pygame.transform.rotate(self.img, self.degree)
        self.img_rect = rot_img.get_rect(center=self.img_rect.center)

        # Copy image to screen
        self.screen.fill((0, 0, 0))
        self.screen.blit(rot_img, self.img_rect)

        # Convert Pygame surface to QImage
        img_data = pygame.image.tostring(self.screen, 'RGB')
        qimage = QImage(
            img_data,
            self.screen.get_width(),
            self.screen.get_height(),
            QImage.Format_RGB888
        )

        # Convert QImage to QPixmap
        qpixmap = QPixmap.fromImage(qimage)

        # Clear the scene and update the display
        self.scene.clear()
        self.scene.addPixmap(qpixmap)
        self.setSceneRect(QRectF(qpixmap.rect()))

        self.degree += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = PygameGraphicsView()
    view.show()
    sys.exit(app.exec_())

