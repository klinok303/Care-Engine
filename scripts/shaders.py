import moderngl

vert_default = """
#version 330 core

in vec2 vert;
in vec2 texcoord;
out vec2 uvs;

void main() {
    uvs = texcoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}
"""

frag_default = """
#version 330 core 

uniform sampler2D tex;

in vec2 uvs;
out vec4 f_color;

void main() {
    f_color = vec4(texture(tex, uvs).rgb, 1.0);
}
"""

frag_retro = """
#version 330 core

uniform sampler2D tex;
uniform float time;

in vec2 uvs;
out vec4 f_color;

vec4 sample_screen(vec2 coords){
    vec4 outcolor = texture(tex, coords.xy);
    if(coords.x<0||coords.y<0||coords.x>1||coords.y>1) outcolor = vec4(0,0,0,1);

    if(fract(coords.y*50)<.25) outcolor *= 0;


    if(fract(coords.x*200)<.33) outcolor.gb = vec2(0,0);
    else if(fract(coords.x*200)>.66) outcolor.rg =vec2(0,0);
    else outcolor.rb = vec2(0,0);
    outcolor *= 3;

    return outcolor;
}

vec4 sample_screen2(vec2 coords){
    vec4 outcolor = texture(tex, coords.xy);
    if(coords.x<0||coords.y<0||coords.x>1||coords.y>1) outcolor = vec4(0,0,0,1);

    outcolor *= min(1, max(.3,(sin(coords.y*400 - time * 20)) + 1.8));

    outcolor.r *= min(1, max(.8,(sin(coords.x*1000 )) + .2));
    outcolor.g *= min(1, max(.8,(sin(coords.x*1000+ 2.094)) + .2));
    outcolor.b *= min(1, max(.8,(sin(coords.x*1000+ 4.189)) + .2));
    outcolor *= 1.2;

    /*if(fract(coords.x*200)<.33) outcolor.gb = vec2(0,0);
    else if(fract(coords.x*200)>.66) outcolor.rg =vec2(0,0);
    else outcolor.rb = vec2(0,0);
    outcolor *= 3;*/

    return outcolor;
}

void main() {
    vec2 uv = uvs;
    uv.xy = (uv.xy - .5) * 2.0;
    uv.x *= 1+pow(abs(uv.y)/3.5, 2.0);//*ratio.x;
    uv.y *= 1+pow(abs(uv.x)/3.5, 2.0);//*ratio.y;

    uv.xy = (uv.xy * .5) + .5;

    vec4 outcolor = sample_screen2(uv.xy) * 3
        + sample_screen2(uv.xy + vec2( 1,0)/1200.0)*2 
        + sample_screen2(uv.xy + vec2(-1,0)/1200.0)*2
        + sample_screen2(uv.xy + vec2( 2,0)/1200.0)*1
        + sample_screen2(uv.xy + vec2(-2,0)/1200.0)*1
    ;
    outcolor /= 9;

    outcolor *= min(1.2, 1.0-pow(length(uv.xy - .5)*1.2, 2));

    outcolor.a = 1.0;
    f_color = outcolor;
}
"""

glitch_frag = """
#version 330 core 

const vec2 intensity = vec2(0.005, 0.005);

uniform sampler2D tex;

in vec2 uvs;
out vec4 f_color;

void main() {
    f_color = vec4
    (
        texture(tex, uvs.xy - vec2(intensity.x, 0.0)).r,
        texture(tex, uvs.xy - vec2(0.0, -intensity.y)).g,
        texture(tex, uvs.xy - vec2(-intensity.x, 0.0)).b,
        0.0
    );
}
"""


def surf_to_texture(surf, ctx):
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = 'BGRA'
    tex.write(surf.get_view('1'))
    return tex
