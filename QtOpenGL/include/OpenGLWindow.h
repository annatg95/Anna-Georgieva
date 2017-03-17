#ifndef OPENGLWINDOW_H_
#define OPENGLWINDOW_H_
#include <QOpenGLWindow>


class OpenGLWindow : public QOpenGLWindow
{
        Q_OBJECT;
    public:
        OpenGLWindow();
        ~OpenGLWindow();

        void paintGL() override;
        void initializeGL() override ;
        void resizeGL(int _w, int _h) override;
        void keyPressEvent(QKeyEvent *_event) override;
        void timerEvent(QTimerEvent *_event) override;

    private:

    int m_width=1024;
    int m_height=720;
    float m_rotY=0.0f;
    int posX=0;
    int posY=0;
    int posZ=0;

    void drawTriangle(int _pX, int _pY, int _pZ);
};


#endif
