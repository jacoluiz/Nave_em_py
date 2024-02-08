import pygame
import os
import threading

class AnimacaoExplosao:
    def __init__(self):
        self.spritesheet = pygame.image.load(os.path.join("sprites", "explosao.png"))
        self.frames = []
        self.current_frame = 0
        self.frame_rate = 15
        self.last_update = pygame.time.get_ticks()
        self.concluido = False

        self.carregar_frames()

    def carregar_frames(self):
        largura_frame = 32
        altura_frame = 32
        for coluna in range(0, self.spritesheet.get_width(), largura_frame):
            self.frames.append(self.spritesheet.subsurface((coluna, 0, largura_frame, altura_frame)))

    def executar_animacao(self, tela, posicao):
        self.concluido = False
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()

        # Iniciando a execução da animação em uma thread separada
        threading.Thread(target=self._animacao_thread, args=(tela, posicao)).start()

    def _animacao_thread(self, tela, posicao):
        while not self.concluido:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return

            tela.blit(self.frames[self.current_frame], posicao)
            pygame.display.flip()

            self.atualizar()

            if self.current_frame == len(self.frames) - 1:
                self.concluido = True

    def atualizar(self):
        agora = pygame.time.get_ticks()
        if agora - self.last_update > 1000 / self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = agora
