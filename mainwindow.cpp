/****************************************************************************
**
** Copyright (C) 2016 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the examples of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:BSD$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** BSD License Usage
** Alternatively, you may use this file under the terms of the BSD license
** as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of The Qt Company Ltd nor the names of its
**     contributors may be used to endorse or promote products derived
**     from this software without specific prior written permission.
**
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
** $QT_END_LICENSE$
**
****************************************************************************/

#include "mainwindow.h"
#include <QtWebEngineWidgets>
#include <QtWidgets>

MainWindow::MainWindow()
{
    setAttribute(Qt::WA_DeleteOnClose, true);

    view = new QWebEngineView(this);

    // file: MyWebEngineView.cpp, MyWebEngineView extends QWebEngineView
    QWebChannel *channel = new QWebChannel(view->page());

    // set the web channel to be used by the page
    // see http://doc.qt.io/qt-5/qwebenginepage.html#setWebChannel
    view->page()->setWebChannel(channel);

    // register QObjects to be exposed to JavaScript
    channel->registerObject(QStringLiteral("jshelper"), this);

    view->load(QUrl("qrc:index"));

    setCentralWidget(view);
}

Q_INVOKABLE void MainWindow::get_elements()
{
    qDebug() << "DONE";
    QString code = QStringLiteral("jQuery('div[name=\"elements\"]').next().text('gfndjkgbfdjgb')");
    qDebug() << "DONE";
    view->page()->runJavaScript(code);
    qDebug() << "DONE";
}

Q_INVOKABLE void MainWindow::send_graph(QVariant s)
{
    QJsonObject jsonObj = s.toJsonObject(); // assume this has been populated with Json data
    QJsonDocument doc(jsonObj);
    QString strJson(doc.toJson(QJsonDocument::Compact));

    qDebug() << "heyyyyyy" << s.toString();
    qDebug() << "heyyyyyy" << QJsonDocument(s.toJsonObject()).toJson(QJsonDocument::Compact).toStdString().c_str();
    qDebug() << "heyyyyyy" << doc.object().value("drawflow");
}

//void MainWindow::adjustLocation()
//{
//    locationEdit->setText(view->url().toString());
//}

//void MainWindow::changeLocation()
//{
//    QUrl url = QUrl::fromUserInput(locationEdit->text());
//    view->load(url);
//    view->setFocus();
//}

//void MainWindow::adjustTitle()
//{
//    if (progress <= 0 || progress >= 100)
//        setWindowTitle(view->title());
//    else
//        setWindowTitle(QStringLiteral("%1 (%2%)").arg(view->title()).arg(progress));
//}

//void MainWindow::setProgress(int p)
//{
//    progress = p;
//    adjustTitle();
//}

//void MainWindow::finishLoading(bool)
//{
//    progress = 100;
//    adjustTitle();
//    view->page()->runJavaScript(jQuery);

//    rotateImages(rotateAction->isChecked());
//}

//void MainWindow::highlightAllLinks()
//{
//    QString code = QStringLiteral("qt.jQuery('a').each( function () { qt.jQuery(this).css('background-color', 'yellow') } )");
//    view->page()->runJavaScript(code);
//}

//void MainWindow::rotateImages(bool invert)
//{
//    QString code;

//    if (invert)
//        code = QStringLiteral("qt.jQuery('img').each( function () { qt.jQuery(this).css('transition', 'transform 2s'); qt.jQuery(this).css('transform', 'rotate(180deg)') } )");
//    else
//        code = QStringLiteral("qt.jQuery('img').each( function () { qt.jQuery(this).css('transition', 'transform 2s'); qt.jQuery(this).css('transform', 'rotate(0deg)') } )");
//    view->page()->runJavaScript(code);
//}

//void MainWindow::removeGifImages()
//{
//    QString code = QStringLiteral("qt.jQuery('[src*=gif]').remove()");
//    view->page()->runJavaScript(code);
//}

//void MainWindow::removeInlineFrames()
//{
//    QString code = QStringLiteral("qt.jQuery('iframe').remove()");
//    view->page()->runJavaScript(code);
//}

//void MainWindow::removeObjectElements()
//{
//    QString code = QStringLiteral("qt.jQuery('object').remove()");
//    view->page()->runJavaScript(code);
//}

//void MainWindow::removeEmbeddedElements()
//{
//    QString code = QStringLiteral("qt.jQuery('embed').remove()");
//    view->page()->runJavaScript(code);
//}
