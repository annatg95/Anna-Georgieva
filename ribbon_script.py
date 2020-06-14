import maya.cmds as cmds


size_h=l/r_leg_stretch_distShape.distance =14.0419
def ribbon_fuction(size_w, size_h):
    nurbsPlane -p 0 0 0 -ax 0 1 0 -w size_w -lr size_h -d 3 -u 1 -v 8 -ch 1;
    #place the nurbs to the leg position and orientation
    #create folicles
    createHair 1 9 10 0 0 1 0 5 0 1 2 1;
    select -r hairSystem1 ;
    select -add pfxHair1 ;
    select -add nucleus1 ;
    select -add curve2 ;
    select -add curve3 ;
    select -add curve4 ;
    select -add curve5 ;
    select -add curve6 ;
    select -add curve7 ;
    select -add curve8 ;
    select -add curve9 ;
    select -add curve10 ; delete

    create joints
    orient x y z the same like the hierarchy
    parent under folicles and zero translations
    insert isopalms in the middle
    duplicate 2 times nurbsPlane

    rename sin twist
    create a blendshape
    duplicate 5 joints prez 2 ot original hierarchy
    rename
    root lower knee upper end
    create grps offset
    parent constraint joints to grps
    parent the joints under the groups
    upper and lower aim groups
    create nurbscircles
    parent under the aim gros lower and upper and under the knee grp, parent joints
    bind skin to the joints
    parent constaint the main shoulder to rot offset grp
    inbetween point constain root knee lower upper offsets
    two new groups upper aimpoint=under root, lower aimpoint=under middle/knee . zero transforms
