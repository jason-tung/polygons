from display import *
from matrix import *
from draw import *
import os

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:

         sphere: add a sphere to the POLYGON matrix -
                 takes 4 arguemnts (cx, cy, cz, r)
         torus: add a torus to the POLYGON matrix - 
                takes 5 arguemnts (cx, cy, cz, r1, r2)
         box: add a rectangular prism to the POLYGON matrix - 
              takes 6 arguemnts (x, y, z, width, height, depth)	    
         clear: clears the edge and POLYGON matrices

	 circle: add a circle to the edge matrix - 
	         takes 4 arguments (cx, cy, cz, r)
	 hermite: add a hermite curve to the edge matrix -
	          takes 8 arguments (x0, y0, x1, y1, rx0, ry0, rx1, ry1)
	 bezier: add a bezier curve to the edge matrix -
	         takes 8 arguments (x0, y0, x1, y1, x2, y2, x3, y3)
         line: add a line to the edge matrix -
               takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
         ident: set the transform matrix to the identity matrix -
         scale: create a scale matrix,
                then multiply the transform matrix by the scale matrix -
                takes 3 arguments (sx, sy, sz)
         move: create a translation matrix,
               then multiply the transform matrix by the translation matrix -
               takes 3 arguments (tx, ty, tz)
         rotate: create a rotation matrix,
                 then multiply the transform matrix by the rotation matrix -
                 takes 2 arguments (axis, theta) axis should be x y or z
         apply: apply the current transformation matrix to the edge and POLYGON matrices
         display: clear the screen, then
                  draw the lines of the edge and POLYGON matrices to the screen
                  display the screen
         save: clear the screen, then
               draw the lines of the edge and POLYGON matrices to the screen
               save the screen to a file -
               takes 1 argument (file name)
         quit: end parsing

See the file script for an example of the file format
"""
ARG_COMMANDS = ['box', 'sphere', 'torus', 'circle', 'bezier', 'hermite', 'line', 'scale', 'move', 'rotate', 'save',
                'color']


def parse_file(fname, edges, polygons, transform, screen, color):
    f = open(fname)
    lines = f.readlines()
    transform_edges = new_matrix()
    transform_polygons = new_matrix()
    step = 0.01
    step_3d = 20
    cmd_args = ""
    imgcnt = 36
    for gif_angle in range(imgcnt):
        c = 0
        while c < len(lines):
            line = lines[c].strip()
            # print ':' + line + ':'

            if line in ARG_COMMANDS:
                c += 1
                args = lines[c].strip().split(' ')
            if line == 'sphere':
                # print 'SPHERE\t' + str(args)
                add_sphere(polygons,
                           float(args[0]), float(args[1]), float(args[2]),
                           float(args[3]), step_3d)
            elif line == 'color':
                color = [int(args[0]), int(args[1]), int(args[2])]
                # draw_lines(edges, screen, color)
                # edges = []
                # polygons = []

            elif line == 'torus':
                # print 'TORUS\t' + str(args)
                add_torus(polygons,
                          float(args[0]), float(args[1]), float(args[2]),
                          float(args[3]), float(args[4]), step_3d)

            elif line == 'box':
                # print 'BOX\t' + str([float(k) for k in args])
                add_box(polygons,
                        float(args[0]), float(args[1]), float(args[2]),
                        float(args[3]), float(args[4]), float(args[5]))

            elif line == 'circle':
                # print 'CIRCLE\t' + str(args)
                add_circle(edges,
                           float(args[0]), float(args[1]), float(args[2]),
                           float(args[3]), step)

            elif line == 'hermite' or line == 'bezier':
                # print 'curve\t' + line + ": " + str(args)
                add_curve(edges,
                          float(args[0]), float(args[1]),
                          float(args[2]), float(args[3]),
                          float(args[4]), float(args[5]),
                          float(args[6]), float(args[7]),
                          step, line)
                # print("wonned")

            elif line == 'line':
                # print 'LINE\t' + str(args)

                add_edge(edges,
                         float(args[0]), float(args[1]), float(args[2]),
                         float(args[3]), float(args[4]), float(args[5]))

            elif line == 'scale':
                # print 'SCALE\t' + str(args)
                t = make_scale(float(args[0]), float(args[1]), float(args[2]))
                matrix_mult(t, transform)

            elif line == 'move':
                # print 'MOVE\t' + str(args)
                t = make_translate(float(args[0]), float(args[1]), float(args[2]))
                matrix_mult(t, transform)

            elif line == 'rotate':
                # print 'ROTATE\t' + str(args)
                theta = float(args[1]) * (math.pi / 180)

                if args[0] == 'x':
                    t = make_rotX(theta)
                elif args[0] == 'y':
                    t = make_rotY(theta)
                else:
                    t = make_rotZ(theta)
                matrix_mult(t, transform)

            elif line == 'ident':
                ident(transform)

            elif line == 'apply':
                matrix_mult(transform, edges)
                matrix_mult(transform, polygons)

            elif line == 'clear':
                edges = []
                polygons = []
            elif line == 'draw':
                draw_lines(edges, screen, color)
                draw_polygons(polygons, screen, color)
            elif line == 'display' or line == 'save':
                clear_screen(screen)
                # print(color)
                draw_lines(edges, screen, color)
                draw_polygons(polygons, screen, color)
                if line == 'display':
                    display(screen)
                else:
                    save_extension(screen, args[0])

            c += 1
        # reset transformation matrix
        ident(transform)
        ident(transform_edges)
        ident(transform_polygons)
        # move matrix
        mv_e0 = make_translate(-250, -250, 0)
        mv_t0 = make_translate(-250, -250, 0)
        #display(screen)
        matrix_mult(mv_e0, transform_edges)
        matrix_mult(mv_t0, transform_polygons)
        # set up the spin matrix
        theta = float(gif_angle) * (math.pi / 180)
        t = make_rotY(theta * 360/imgcnt)
        matrix_mult(t, transform_edges)
        matrix_mult(t, transform_polygons)
        # move again
        mv_e1 = make_translate(250, 250, 0)
        mv_t1 = make_translate(250, 250, 0)
        matrix_mult(mv_e1, transform_edges)
        matrix_mult(mv_t1, transform_polygons)
        # apply matricies
        matrix_mult(transform_edges, edges)
        matrix_mult(transform_polygons, polygons)
        # matrix_mult(transform, edges)
        # matrix_mult(transform, polygons)
        # draw
        draw_lines(edges, screen, color)
        draw_polygons(polygons, screen, color)
        # display(screen)
        # save
        file_name = "gif" + str(gif_angle) + ".png"
        save_extension(screen, file_name)
        cmd_args += file_name + " "
        # restart
        clear_screen(screen)
        edges = []
        polygons = []

    cmd = "convert -delay 3x100 -loop 0 " + cmd_args + "epic.gif"
    # print(cmd)
    os.system(cmd)
    os.system("rm *.png")

