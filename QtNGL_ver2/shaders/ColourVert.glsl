#version 450

layout(location=0) in vec3 inPos;
layout(location=1) in vec3 inColour;


uniform mat4 MVP;
out vec3 colour;


void main()
{
    colour=inColour;
    gl_Position = MVP*vec4(inPos, 1.0);
}
