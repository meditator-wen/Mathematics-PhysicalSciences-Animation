from manim import *
import random

from colour import Color

class ProjectileMotionExample3D(ThreeDScene):
   
    def construct(self):
        color_choice_list=[YELLOW,RED,PURE_RED,PINK,ORANGE,WHITE]
        self.set_camera_orientation(phi=2*PI/5, theta=PI/5)
        x_length_const=14
        y_length_const=14
        z_length_const=8
        init_velocity=20 #20m/s
        time_step=0.1 # 0.1 second
        time_start=0
        time_stop=5
        angle_start=0 # 
        angle_end=2*np.pi
        angel_step=np.pi/18
        gravity_const=10 #10m/s^2
        resistence=0.15 # 阻力系数
        ax = ThreeDAxes(
            x_range=[-80, 80, 20],
            y_range=[-80, 80, 20],
            z_range=[-25, 25, 8],
            x_length=x_length_const,
            y_length=y_length_const,
            z_length=z_length_const,
            tips=True,
            axis_config={"include_numbers": True,'tip_shape': StealthTip,'stroke_width':0.5}
        )           

        labels = ax.get_axis_labels(
            Tex("x-axis").scale(0.7), Text("y-axis").scale(0.45), Text("z-axis").scale(0.45)
        )
        self.add(ax, labels)

        # fontsize=18

        # para=Text("阻力系数k=0.15",font_size=fontsize)
        # self.play(para.animate.shift(np.array((-6, 3, 0.0)))) 

        dot_group_init=VGroup(*[Dot((0,0,-3),0.03,color=RED) 
                                for _ in np.arange(angle_start,angle_end,angel_step)])
        
        self.add(dot_group_init)

        for dot in dot_group_init:
            self.add(TracedPath(dot.get_center,stroke_width=1.1,stroke_color=dot.get_color(), dissipating_time=5*time_step, stroke_opacity=[0, 1])) # , stroke_opacity=[0, 1])

        dot_group_original=VGroup(*[Dot((0,0,0),0.03,color=RED) for _ in np.arange(angle_start,angle_end,angel_step)])

        self.play(Transform(dot_group_init,dot_group_original,path_func=utils.paths.straight_path(),run_time=30*time_step))   
        
        dot_group_original_projectile=VGroup()
        
        for fir in np.arange(angle_start,angle_end,angel_step):
            for second in np.arange(angle_start,angle_end,angel_step):
                dot_group_original_projectile.add(Dot((0,0,0),0.006,color=random.choice(color_choice_list)))
                
        # self.add(dot_group_original_projectile)
        for dot in dot_group_original_projectile:
            self.add(TracedPath(dot.get_center,stroke_width=0.4,stroke_color=dot.get_color(), dissipating_time=40000*time_step, stroke_opacity=[0.8, 1])) # , stroke_opacity=[0, 1])

        for t in np.arange(time_start,time_stop,time_step):
            dot_group_temp=VGroup()
            for theta in np.arange(angle_start,angle_end+angel_step,angel_step):

                for gama in np.arange(angle_start,angle_end+angel_step,angel_step):
                    x_pos=init_velocity*np.cos(theta)*np.cos(gama)*t*x_length_const/(ax.x_range[1]-ax.x_range[0])
                    y_pos=init_velocity*np.cos(theta)*np.sin(gama)*t*y_length_const/(ax.y_range[1]-ax.y_range[0])
                    z_pos=(init_velocity*np.sin(theta)*t-0.5*gravity_const*(t**2))*z_length_const/(ax.z_range[1]-ax.z_range[0])
                    dot_temp=Dot((x_pos,y_pos,z_pos),0.006,color=RED)
                    dot_group_temp.add(dot_temp)

                    # # 有风阻情况下x轴运动方程
                    # x_pos_resistence=(1/resistence)*init_velocity*np.cos(theta)*np.cos(gama)*(1-np.exp((-1)*resistence*t))*x_length_const/(ax.x_range[1]-ax.x_range[0])
                    # # 有风阻情况下y轴运动方程
                    # y_pos_resistence=(1/resistence)*init_velocity*np.cos(theta)*np.sin(gama)*(1-np.exp((-1)*resistence*t))*y_length_const/(ax.y_range[1]-ax.y_range[0])
                    # # 有风阻情况下Z轴运动方程
                    # z_pos_resistence=(1/resistence)*(init_velocity*np.sin(theta)+gravity_const/resistence)*(1-np.exp((-1)*resistence*t))-t*gravity_const/resistence
                    # z_pos_resistence=z_pos_resistence*y_length_const/(ax.y_range[1]-ax.y_range[0])
                    # dot_temp_resistence=Dot((x_pos_resistence,y_pos_resistence,z_pos_resistence),0.006,color=RED)
                    # dot_group_temp.add(dot_temp_resistence)
                
   
            self.play(Transform(dot_group_original_projectile,dot_group_temp,path_func=utils.paths.straight_path(),run_time=time_step)) 
        
        # 三维抛体包络面
        resolution_fa = 40
        def param_surface(u, v):
            x = u
            y = v
            z = 20-(1/80)*(x**2+y**2)
            return z
        surface_plane = Surface(
            lambda u, v: ax.c2p(u, v, param_surface(u, v)),
            resolution=(resolution_fa, resolution_fa),
            v_range=[ax.x_range[0],ax.x_range[1]],
            u_range=[ax.y_range[0],ax.y_range[1]],
            )
        surface_plane.set_style(fill_opacity=0.8)
        # surface_plane.set_fill_by_value(axes=ax, colorscale=[(RED, -0.5), (YELLOW, 0), (GREEN, 0.5)], axis=2)
        # border_line_function=lambda x: 20-(1/80)*x**2
        # plot_graph=ax.plot(border_line_function,[ax.x_range[0],ax.x_range[1],0.1], use_smoothing=False).set_stroke(width=0.9)
        self.play(Create(surface_plane),run_time=1)
        self.wait
        


        
        