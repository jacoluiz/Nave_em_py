import pygame

def checarTeclado(fechar_jogo, nave, ia_jogando ):
    if not ia_jogando:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fechar_jogo = False

        if keys[pygame.K_a]:
            nave.rotacionar(5)
        if keys[pygame.K_d]:
            nave.rotacionar(-5)
        if keys[pygame.K_w]:
            nave.ativar_boost()
        if keys[pygame.K_s]:
            pass
        if keys[pygame.K_ESCAPE]:
            fechar_jogo = False

    return fechar_jogo