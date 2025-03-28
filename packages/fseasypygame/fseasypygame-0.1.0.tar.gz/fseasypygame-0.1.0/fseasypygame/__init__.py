import os
import sys
import time
import pygame

# ==================== 全局工具部分 ====================
_image_cache = {}
_default_image = pygame.Surface((50, 50))
_default_image.fill((255, 0, 0))


def _load_image(img_path, width=None, height=None):
    """智能图片加载函数"""
    cache_key = f"{img_path}_{width}_{height}"

    if cache_key in _image_cache:
        return _image_cache[cache_key]

    try:
        image = pygame.image.load(img_path).convert_alpha()
        orig_w, orig_h = image.get_size()

        if width is not None or height is not None:
            if width is None:
                width = int(orig_w * (height / orig_h))
            elif height is None:
                height = int(orig_h * (width / orig_w))
            image = pygame.transform.smoothscale(image, (width, height))

        _image_cache[cache_key] = image
        return image
    except Exception as e:
        print(f"图片加载失败: {img_path} - {str(e)}")
        error_img = _default_image.copy()
        if width or height:
            error_img = pygame.transform.smoothscale(error_img,
                                                     (width or 50, height or 50))
        font = pygame.font.SysFont("Arial", 12)
        text = font.render("Missing", True, (255, 255, 255))
        error_img.blit(text, (5, 5))
        _image_cache[cache_key] = error_img
        return error_img


# ==================== 核心类实现 ====================
class Animation:
    def __init__(self, frame_paths, frame_rate=10,
                 destroy=False, revert=True,
                 width=None, height=None, repeat=1):
        self.frames = [_load_image(p, width, height) for p in frame_paths]
        self.frame_rate = frame_rate
        self.current_frame = 0
        self.frame_count = 0
        self.destroy = destroy
        self.revert = revert
        self.repeat = repeat
        self.repeat_count = 0

    def update(self):
        self.frame_count += 1
        if self.frame_count % self.frame_rate == 0:
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.repeat_count += 1
                if self.repeat_count >= self.repeat and self.repeat != -1:
                    return True
                self.current_frame = 0
        return False


class GameText:
    def __init__(self, text, x=0, y=0, font_size=24, color=(0, 0, 0)):
        self._raw_text = text
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont("simhei", font_size)
        self.color = color
        self.visible = True
        self._bindings = {}
        self._auto_update = True

        if game_instance:
            game_instance.add_game_text(self)

    def bind(self, var_name, target_obj, attr_name=None):
        if attr_name is None:
            attr_name = var_name
        self._bindings[var_name] = lambda: getattr(target_obj, attr_name, "N/A")

    def bind_func(self, var_name, value_func):
        self._bindings[var_name] = value_func

    def unbind(self, var_name):
        if var_name in self._bindings:
            del self._bindings[var_name]

    def toggle_auto_update(self, enable=True):
        self._auto_update = enable

    def _generate_text(self):
        try:
            values = {k: v() if callable(v) else v for k, v in self._bindings.items()}
            return self._raw_text.format(**values)
        except Exception as e:
            print(f"文本生成错误: {str(e)}")
            return self._raw_text

    def set_text(self, text):
        self._raw_text = text

    def set_font_size(self, size):
        self.font = pygame.font.SysFont("simhei", size)

    def set_color(self, color):
        self.color = color

    def toggle_visibility(self):
        self.visible = not self.visible

    def draw(self, surface):
        if self.visible:
            final_text = self._generate_text() if self._auto_update and self._bindings else self._raw_text
            text_surface = self.font.render(final_text, True, self.color)
            surface.blit(text_surface, (self.x, self.y))

    def destroy(self):
        if game_instance:
            game_instance.remove_game_text(self)


class GroupManager:
    def __init__(self):
        self.groups = {}

    def get_all_group_names(self):
        return list(self.groups.keys())

    def get_group(self, name):
        if name not in self.groups:
            self.groups[name] = pygame.sprite.Group()
        return self.groups[name]

    def add_to_group(self, sprite, name):
        group = self.get_group(name)
        group.add(sprite)
        if not hasattr(sprite, 'groups'):
            sprite.groups = []
        sprite.groups.append(name)

    def remove_from_group(self, sprite, name):
        if name in self.groups:
            self.groups[name].remove(sprite)
            if name in sprite.groups:
                sprite.groups.remove(name)


class KeyStatus:
    def __init__(self):
        self.pressed = False
        self.last_press_time = 0
        self.interval = 0.2
        self.released = False

    def set_interval(self, interval):
        self.interval = interval

    def is_triggered(self):
        return self.pressed

    def is_triggered_with_interval(self):
        now = time.time()
        if self.pressed and now - self.last_press_time > self.interval:
            self.last_press_time = now
            return True
        return False

    def handle_keyup(self):
        self.pressed = False
        self.released = True

    def reset_released(self):
        self.released = False


class Keys:
    key_mapping = {
        '0': pygame.K_0, '1': pygame.K_1, '2': pygame.K_2, '3': pygame.K_3, '4': pygame.K_4,
        '5': pygame.K_5, '6': pygame.K_6, '7': pygame.K_7, '8': pygame.K_8, '9': pygame.K_9,
        'LEFT': pygame.K_LEFT, 'RIGHT': pygame.K_RIGHT, 'UP': pygame.K_UP, 'DOWN': pygame.K_DOWN,
        'SPACE': pygame.K_SPACE,
        **{chr(i): getattr(pygame, f'K_{chr(i).lower()}') for i in range(ord('A'), ord('Z') + 1)}
    }


class GameObject(pygame.sprite.Sprite):
    def __init__(self, img_path, x=0, y=0, width=None, height=None, name=None, group_name=None, rotation=0, **kwargs):
        super().__init__()
        self._original_path = img_path
        self._original_image = _load_image(img_path, width, height)
        self.image = self._original_image.copy()
        if rotation != 0:
            self.image = pygame.transform.rotate(self.image, rotation)
        self._width = self.image.get_width()
        self._height = self.image.get_height()
        self._center_x = x
        self._center_y = y
        self.rect = self.image.get_rect(center=(x, y))
        self._angle = 90
        self._alive = True
        self._animations = {}
        self._current_animation = None
        self._collision_scale = 1.0
        self.collision_groups = []
        self._last_collisions = set()
        self.groups = []
        if group_name:
            group_manager.add_to_group(self, group_name)
        else:
            default_group = os.path.splitext(os.path.basename(img_path))[0]
            group_manager.add_to_group(self, default_group)
        self._init_custom(**kwargs)

    def _init_custom(self, **kwargs):
        pass

    @property
    def x(self):
        return self._center_x - self._width // 2

    @x.setter
    def x(self, value):
        self._center_x = value + self._width // 2;
        self.rect.center = (self._center_x, self._center_y)

    @property
    def y(self):
        return self._center_y - self._height // 2

    @y.setter
    def y(self, value):
        self._center_y = value + self._height // 2;
        self.rect.center = (self._center_x, self._center_y)

    @property
    def center(self):
        return (self._center_x, self._center_y)

    @center.setter
    def center(self, pos):
        self._center_x, self._center_y = pos;
        self.rect.center = pos

    def add_collision_group(self, group_name):
        if group_name not in self.collision_groups:
            self.collision_groups.append(group_name)

    def clear_collision_groups(self):
        self.collision_groups = []

    def _check_auto_collisions(self):
        current_collisions = set()
        for group_name in self.collision_groups:
            group = group_manager.get_group(group_name)
            for sprite in group:
                if sprite != self and pygame.sprite.collide_rect(self, sprite):
                    current_collisions.add(sprite)
        new_collisions = current_collisions - self._last_collisions
        for sprite in new_collisions:
            self.on_collision(sprite)
        if current_collisions:
            self.on_collision_stay(current_collisions)
        ended_collisions = self._last_collisions - current_collisions
        if ended_collisions:
            self.on_collision_end(ended_collisions)
        self._last_collisions = current_collisions

    def on_collision(self, other):
        pass

    def on_collision_stay(self, others):
        pass

    def on_collision_end(self, others):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        if game_instance and game_instance.getDrawRectFlag():
            pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)

    def update(self):
        self._process_animation()
        self._check_auto_collisions()
        self._custom_update()

    def _custom_update(self):
        pass

    def _process_animation(self):
        if self._current_animation:
            finished = self._current_animation.update()
            if finished:
                self._handle_animation_end()

    def _handle_animation_end(self):
        if self._current_animation.destroy:
            self.destroy()
        elif self._current_animation.revert:
            self.image = self._original_image.copy()
        self._current_animation = None

    def destroy(self):
        if self._alive:
            self._alive = False
            if self.group:
                self.group.remove(self)
            self.kill()

    def is_alive(self):
        return self._alive

    def move(self, dx, dy):
        if self._alive:
            self._center_x += dx
            self._center_y += dy
            self.rect.center = (self._center_x, self._center_y)

    def rotate(self, angle):
        if self._alive:
            self._angle += angle
            self.image = pygame.transform.rotate(self._original_image, self._angle - 90)
            self.rect = self.image.get_rect(center=self.rect.center)

    def set_size(self, width=None, height=None):
        if width is None and height is None:
            return
        orig_w, orig_h = self._original_image.get_size()
        if width is None:
            width = int(orig_w * (height / orig_h))
        if height is None:
            height = int(orig_h * (width / orig_w))
        self._width = width
        self._height = height
        self._original_image = _load_image(self._original_path, width, height)
        self.image = self._original_image.copy()
        self.rect = self.image.get_rect(center=self.center)

    def check_collision(self, group_name):
        group = group_manager.get_group(group_name)
        collided = pygame.sprite.spritecollideany(self, group)
        if collided:
            self.on_collide(collided)
        return collided

    def on_collide(self, target):
        pass

    def add_animation(self, name, frame_paths, frame_rate=10, repeat=1, destroy=False, revert=True):
        self._animations[name] = Animation(
            frame_paths, frame_rate=frame_rate, repeat=repeat, destroy=destroy, revert=revert
        )

    def start_animation(self, name):
        if name in self._animations:
            self._current_animation = self._animations[name]
            self._current_animation.current_frame = 0
            self._current_animation.repeat_count = 0

    set_angel = rotate
    getX = lambda self: self._center_x
    getY = lambda self: self._center_y
    getAngel = lambda self: self._angle
    getWidth = lambda self: self._width
    getHeight = lambda self: self._height
    getRect = lambda self: self.rect
    isOutofBorder = lambda self: not self.rect.colliderect(game_instance.screen.get_rect())


class Game:
    def __init__(self, width=800, height=600):
        global game_instance
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.keys = {k: KeyStatus() for k in Keys.key_mapping.keys()}
        self.texts = []
        self.background = None
        self.update_func = None
        self.drawRect = False
        game_instance = self

    def add_game_text(self, text):
        self.texts.append(text)

    def remove_game_text(self, text):
        self.texts.remove(text)

    def setDrawRectFlag(self, flag=True):
        self.drawRect = flag

    def getDrawRectFlag(self):
        return self.drawRect

    def set_bg(self, img_path='bg.png'):
        self.background = _load_image(img_path, self.screen.get_width(), self.screen.get_height())

    def is_key_pressed(self, key):
        return self.keys[key.upper()].is_triggered()

    def is_key_released(self, key):
        return self.keys[key.upper()].released

    def set_update(self, func):
        self.update_func = func

    def toggle_debug(self):
        self.drawRect = not self.drawRect

    def run(self, fps=60):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    key = pygame.key.name(event.key).upper()
                    if key in self.keys:
                        self.keys[key].handle_keyup()
            keys_state = pygame.key.get_pressed()
            for key, status in self.keys.items():
                status.pressed = keys_state[Keys.key_mapping[key]]
            if self.update_func:
                self.update_func()
            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill((0, 0, 0))
            for group in group_manager.groups.values():
                group.update()
                for sprite in group:
                    sprite.draw(self.screen)
            for text in self.texts:
                text.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(fps)
            for status in self.keys.values():
                status.reset_released()


# ==================== 初始化 ====================
group_manager = GroupManager()
game_instance = None
