from mlx import Mlx

def mymouse(button, x, y, mystuff):
    print(f"Got mouse event! button {button} at {x},{y}.")

def mykey(keynum, mystuff):
    print(f"Got key {keynum}, and got my stuff back:")
    print(mystuff)
    if keynum == 32:
        m.mlx_mouse_hook(win_ptr, None, None)



m = Mlx()
def exit_mlx(mlx_ptr):
    m.mlx_loop_exit(mlx_ptr)
mlx_ptr = m.mlx_init()
win_ptr = m.mlx_new_window(mlx_ptr, 800, 800, "toto")
m.mlx_clear_window(mlx_ptr, win_ptr)
m.mlx_string_put(mlx_ptr, win_ptr, 20, 20, 255, "Hello PyMlx!")
(ret, w, h) = m.mlx_get_screen_size(mlx_ptr)
print(f"Got screen size: {w} x {h}, {ret} .")

stuff = [1, 2]
m.mlx_mouse_hook(win_ptr, mymouse, None)
m.mlx_key_hook(win_ptr, mykey, stuff)
m.mlx_hook(win_ptr, 33, 0, exit_mlx, mlx_ptr)

m.mlx_loop(mlx_ptr)