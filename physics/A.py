from manim import *
import random
from colour import Color
class DifferentDensitiesExample(Scene):
     def construct(self):
        color_choice_list=[YELLOW,RED,PURE_RED,PINK,ORANGE,WHITE]
        # color_choice_list=[BLUE,PURE_BLUE,GREEN,PURE_GREEN,YELLOW,RED,PURE_RED,PINK,ORANGE,WHITE]
        x_length_const=14
        y_length_const=8
        init_velocity=20 #20m/s
        time_step=0.1 # 0.1 second
        time_start=0
        time_stop=5
        angle_start=0 # 
        angle_end=2*np.pi
        angel_step=np.pi/10
        gravity_const=10 #10m/s^2
        resistence=0.15 # 阻力系数
        ax = Axes(
            x_range=[-80, 80, 10],
            y_range=[-25, 25, 8],
            x_length=x_length_const,
            y_length=y_length_const,
            tips=True,
            axis_config={"include_numbers": False,'tip_shape': StealthTip,'stroke_width':0.5}
        )
        # self.play(Create(Arrow(start=np.array((0.0, 0.0, 0.0)), end=np.array((0.5, np.sqrt(3)/2, 0.0)),max_stroke_width_to_length_ratio=1)))
     

        dot_group_original=VGroup(*[Dot((0,0,0),0.03,color=RED) for _ in [np.pi/3]])

        self.add(ax)
        x_function = MathTex(r"x=\left( v_0\cos \theta \right) t")
        y_function = MathTex(r"y=\left( v_0\sin \theta \right) t-\frac{1}{2}gt^2")

        self.play(x_function.animate.shift(np.array((4, 1, 0.0)))) 
        self.play(y_function.animate.shift(np.array((0, 2.8, 0.0)))) 

        dot_group_original_projectile=VGroup(*[Dot((0,0,0),0.01,color=Color(rgb=color_to_rgb(random.choice(color_choice_list)))) 
                                for _ in [np.pi/3]])
        # self.add(dot_group_original_projectile)
        for dot in dot_group_original_projectile:
            self.add(TracedPath(dot.get_center,stroke_width=0.8,stroke_color=dot.get_color(), dissipating_time=100000*time_step, stroke_opacity=[0.8, 1])) # , stroke_opacity=[0, 1])

        for t in np.arange(time_start,time_stop,time_step):
            dot_group_temp=VGroup()
            for theta in [np.pi/3]:

                # 无风阻情况下x轴运动方程
                x_pos=init_velocity*np.cos(theta)*t*x_length_const/(ax.x_range[1]-ax.x_range[0])
                # 无风阻情况下y轴轨迹方程
                y_pos=(init_velocity*np.sin(theta)*t-0.5*gravity_const*(t**2))*y_length_const/(ax.y_range[1]-ax.y_range[0])
                z_pos=0
                dot_temp=Dot((x_pos,y_pos,z_pos),0.01,color=RED)

                # 有风阻情况下x轴运动方程
                x_pos_resistence=(1/resistence)*init_velocity*np.cos(theta)*(1-np.exp((-1)*resistence*t)) 
                # 有风阻情况下y轴运动方程
                y_pos_resistence=(1/resistence)*(init_velocity*np.sin(theta)+gravity_const/resistence)*(1-np.exp((-1)*resistence*t))-t*gravity_const/resistence
                dot_temp_resistence=Dot((x_pos_resistence,y_pos_resistence,z_pos),0.006,color=RED)
                

                dot_group_temp.add(dot_temp)
                
            self.play(Transform(dot_group_original_projectile,dot_group_temp,path_func=utils.paths.straight_path(),run_time=time_step)) 
            
       
        # border_line_function=lambda x: 20-(1/80)*x**2
        # plot_graph=ax.plot(border_line_function,[ax.x_range[0],ax.x_range[1],0.1], use_smoothing=False).set_stroke(width=0.9)
        
        # self.play(Create(plot_graph),run_time=2) 
        self.wait
        
        