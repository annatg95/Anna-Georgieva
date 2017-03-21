#ifndef NGLSCENE_H_
#define NGLSCENE_H_

#include <ngl/Camera.h>
#include <ngl/BBox.h>
#include <ngl/SimpleVAO.h>
#include <ngl/Transformation.h>
#include <ngl/Vec3.h>
#include <ngl/Text.h>
#include "WindowParams.h"
#include <QEvent>
#include <QResizeEvent>
#include <QOpenGLWidget>
#include <memory>

class NGLScene : public QOpenGLWidget
{
Q_OBJECT        // must include this if you use Qt signals/slots
public :
    NGLScene(QWidget *_parent );
    ~NGLScene();
 public slots :

    void setColour();
   // void addBoid();
   // void removeBoid();

protected:
    ngl::Mat4 m_mouseGlobalTX;
    WinParams m_win;
    ngl::Vec3 m_modelPos;
    ngl::Camera m_cam;
    ngl::Transformation m_transform;

    void initializeGL();
    void resizeGL(int _w , int _h);
    void paintGL();

private :
    std::unique_ptr<ngl::BBox> m_bbox;
    std::unique_ptr<ngl::AbstractVAO> m_vao;
    //    std::unique_ptr<ngl::VertexArrayObject> m_vao;

    void mouseMoveEvent (QMouseEvent * _event );
    void mousePressEvent ( QMouseEvent *_event);
    void mouseReleaseEvent ( QMouseEvent *_event );
    void wheelEvent( QWheelEvent *_event);

    void loadMatricesToShader();
    void loadMatricesToColourShader();

       void buildVAO();

};

#endif
