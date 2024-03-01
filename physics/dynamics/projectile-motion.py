from manim import *
import random
from colour import Color

class ProjectileMotionExample(Scene):
   
    def construct(self):
        color_choice_list=[YELLOW,RED,PURE_RED,ORANGE,WHITE] #PINK
        # color_choice_list=[BLUE,PURE_BLUE,GREEN,PURE_GREEN,YELLOW,RED,PURE_RED,PINK,ORANGE,WHITE]
        x_length_const=14
        y_length_const=8
        init_velocity=20 #20m/s
        time_step=0.1 # 0.1 second
        time_start=0
        time_stop=5
        angle_start=0 # 
        angle_end=2*np.pi
        angel_step=np.pi/60
        gravity_const=10 #10m/s^2
        resistence=0.15 # 阻力系数
        ax = Axes(
            x_range=[-80, 80, 10],
            y_range=[-25, 25, 8],
            x_length=x_length_const,
            y_length=y_length_const,
            tips=True,
            axis_config={"include_numbers": True,'tip_shape': StealthTip,'stroke_width':0.5}
        )
        # border_line_function = FunctionGraph(
        #     lambda x: (init_velocity**2/(2*gravity_const)-gravity_const*x**2/2*(init_velocity**2)),
        #     x_range=[ax.x_range[0],ax.x_range[1],0.1],
        #     color=GREEN,
        # )
        
        #     lambda x: (init_velocity**2/(2*gravity_const)-gravity_const*x**2/2*(init_velocity**2)),
     
    
        dot_group_init=VGroup(*[Dot((0,-3,0),0.03,color=RED) 
                                for _ in np.arange(angle_start,angle_end,angel_step)])
        
        self.add(dot_group_init)

        fontsize=18

        para=Text("阻力系数k=0.15",font_size=fontsize)
        self.play(para.animate.shift(np.array((-6, 3, 0.0)))) 

        for dot in dot_group_init:
            self.add(TracedPath(dot.get_center,stroke_width=1.1,stroke_color=dot.get_color(), dissipating_time=4*time_step, stroke_opacity=[0, 1])) # , stroke_opacity=[0, 1])

        dot_group_original=VGroup(*[Dot((0,0,0),0.03,color=RED) for _ in np.arange(angle_start,angle_end,angel_step)])

        self.play(Transform(dot_group_init,dot_group_original,path_func=utils.paths.straight_path(),run_time=30*time_step))   
        self.remove(dot_group_init)
        self.add(ax)

        dot_group_original_projectile=VGroup(*[Dot((0,0,0),0.006,color=Color(rgb=color_to_rgb(random.choice(color_choice_list)))) 
                                for _ in np.arange(angle_start,angle_end,angel_step)])
        # self.add(dot_group_original_projectile)
        for dot in dot_group_original_projectile:
            self.add(TracedPath(dot.get_center,stroke_width=0.4,stroke_color=dot.get_color(), dissipating_time=100000*time_step, stroke_opacity=[0.8, 1])) # , stroke_opacity=[0, 1])

        for t in np.arange(time_start,time_stop,time_step):
            dot_group_temp=VGroup()
            for theta in np.arange(angle_start,angle_end+angel_step,angel_step):

                # 无风阻情况下x轴运动方程
                x_pos=init_velocity*np.cos(theta)*t*x_length_const/(ax.x_range[1]-ax.x_range[0])
                # 无风阻情况下y轴轨迹方程
                y_pos=(init_velocity*np.sin(theta)*t-0.5*gravity_const*(t**2))*y_length_const/(ax.y_range[1]-ax.y_range[0])
                z_pos=0
                dot_temp=Dot((x_pos,y_pos,z_pos),0.006,color=RED)

                # 有风阻情况下x轴运动方程
                x_pos_resistence=(1/resistence)*init_velocity*np.cos(theta)*(1-np.exp((-1)*resistence*t))*x_length_const/(ax.x_range[1]-ax.x_range[0]) 
                # 有风阻情况下y轴运动方程
                y_pos_resistence=(1/resistence)*(init_velocity*np.sin(theta)+gravity_const/resistence)*(1-np.exp((-1)*resistence*t))-t*gravity_const/resistence
                y_pos_resistence=y_pos_resistence*y_length_const/(ax.y_range[1]-ax.y_range[0])
                dot_temp_resistence=Dot((x_pos_resistence,y_pos_resistence,z_pos),0.006,color=RED)
                

                dot_group_temp.add(dot_temp)
                
            self.play(Transform(dot_group_original_projectile,dot_group_temp,path_func=utils.paths.straight_path(),run_time=time_step)) 
            

        border_line_function=lambda x: 20-(1/80)*x**2
        plot_graph=ax.plot(border_line_function,[ax.x_range[0],ax.x_range[1],0.1], use_smoothing=False).set_stroke(width=0.9)
        
        self.play(Create(plot_graph),run_time=2) 
        desc=Text("白色线为无空气阻力下抛体轨迹的外切线，白色线内部是有空气阻力下抛体的运动轨迹线，轨迹整体被压缩了",font_size=16).next_to(plot_graph,UP)
        
        self.play(Create(desc),run_time=1) 
        self.wait
        
        