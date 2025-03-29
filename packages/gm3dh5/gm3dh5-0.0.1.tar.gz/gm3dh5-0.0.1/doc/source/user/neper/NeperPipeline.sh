neper -T -loadtesr Al.tesr -transform autocrop,resetorigin,renumber,resetcellid -o Al-c
neper -V Al-c.tesr -datavoxcol ori -datavoxcolscheme ipf -print Al-c -cameraprojection orthographic -cameracoo x+8:y:z -print Al-c-x -cameracoo x:y+8:z -print Al-c-y -cameracoo x:y:z+8 -print Al-c-z
neper -V Al-c.tesr -datavoxcol ori -datavoxcolscheme ipf -showcell "z>0.4&&z<0.6&&y>0.06&&y<0.18&&x>0.14&&x<0.3" -cameracoo x+length*vx/6:y+length*vy/6:z+length*vz/6 -imagesize 600:600 -print Al-c-center
#neper -V Al-c.tesr -datavoxcol ori -datavoxcolscheme ipf -showcell "(z>0.4&&z<0.6&&y>0.06&&y<0.18&&x>0.14&&x<0.3&&id!=666&&id!=881&&id!=1008)||(id==704)||(id==1005)" -cameracoo x+length*vx/6:y+length*vy/6:z+length*vz/6 -imagesize 600:600 -print Al-c-center
neper -T -n 1000 -domain "cube(0.44,0.24,1.00):translate(0,0,0)" -o domain
neper -T -loadtesr Al-c.tesr -transform "grow,tessinter(domain.tess),autocrop,renumber" -o Al-cf
neper -T -loadtesr Al-cf.tesr -transform "rmsat,grow,tessinter(domain.tess)" -o Al-cfs
neper -V domain.tess -showcell 0 -showedge "domtype==1" -showface "domtype==2" -dataedgerad 0.0035 -datafacetrs 0.5 -imageformat pov:objects -print domain
neper -V Al-cfs.tesr -includepov domain.pov -datavoxcol ori -datavoxcolscheme ipf -print Al-cfs -cameraprojection orthographic -cameracoo x+8:y:z -print Al-cfs-x -cameracoo x:y+8:z -print Al-cfs-y -cameracoo x:y:z+8 -print Al-cfs-z
neper -T -n from_morpho -domain "cube(0.44,0.24,1.00):translate(0,0,0)" -morpho "tesr:file(Al-cfs.tesr)" -morphooptiobj "tesr:pts(region=surf,res=10)" -ori from_morpho -crysym cubic -o Al
# crysym cubic added to Al.tess
neper -T -loadtess Al.tess -reg 1 -rsel 0.25 -o Al-r
neper -V Al-r.tess -datacellcol ori -datacellcolscheme ipf -print Al-tess
neper -V Al-r.tess -datacellcol ori -datacellcolscheme ipf -showcell "z>0.4&&z<0.6&&y>0.06&&y<0.18&&x>0.14&&x<0.3" -cameracoo x+length*vx/6:y+length*vy/6:z+length*vz/6 -imagesize 600:600 -print Al-tess-center
neper -M Al-r.tess -rcl 0.5 -pl 8
neper -V Al-r.tess,Al-r.msh -showelt1d all -dataelset3dcol ori -dataelset3dcolscheme ipf -print Al-mesh
neper -V Al-r.tess,Al-r.msh -showelset "z>0.4&&z<0.6&&y>0.06&&y<0.18&&x>0.14&&x<0.3" -showelt1d elt3d_shown -dataelset3dcol ori -dataelset3dcolscheme ipf -cameracoo x+length*vx/6:y+length*vy/6:z+length*vz/6 -imagesize 600:600 -print Al-mesh-center
