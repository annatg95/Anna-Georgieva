#ifndef NGLSCENE_H_
#define NGLSCENE_H_

#include <ngl/BBox.h>
#include <ngl/Camera.h>
#include <ngl/Transformation.h>
#include <ngl/ShaderLib.h>
#include "Boid.h"
#include "WindowParams.h"
#include <QEvent>
#include <QResizeEvent>
#include <QOpenGLWidget>
#include <memory>

#include <ngl/Vec3.h>
#include "Emitter.h"



class NGLScene : public QOpenGLWidget
{
Q_OBJECT        // must include this if you use Qt signals/slots
public :
    NGLScene(QWidget *_parent, int _numOfBoids );
    ~NGLScene();
    void initializeGL();
    void resizeGL(int _w , int _h);
    void paintGL();

 public slots :
    void addBoid();
    void removeBoid();
    void setColour();

protected:
    ngl::Mat4 m_mouseGlobalTX;
    WinParams m_win;
    ngl::Vec3 m_modelPos;
    ngl::Camera m_cam;
    ngl::Transformation m_transform;

    int m_numOfBoids;
    int m_boidUpdateTimer;
    bool m_animate;

private :
    std::unique_ptr<ngl::BBox> m_bbox;
    std::vector<Boid> m_boidArray;



    void mouseMoveEvent (QMouseEvent * _event );
    void mousePressEvent ( QMouseEvent *_event);
    void mouseReleaseEvent ( QMouseEvent *_event );
    void wheelEvent( QWheelEvent *_event);
    void timerEvent(QTimerEvent *) override;


    void loadMatricesToShader();
    void loadMatricesToColourShader();

    void buildVAO();
    //collisions
    void resetBoids();
     void BBoxCollision();

     std::unique_ptr<Emitter> m_emitter;



};

#endif
