# -*- coding: utf-8 -*-
# @Author: durban.zhang
# @Date:   2019-11-13 16:30:07
# @Last Modified by:   durban.zhang
# @Last Modified time: 2019-11-28 10:41:14
from flask_mail import Message
from baby.extensions import mail
from baby import create_app
from baby.celery import create_celery
celery = create_celery(create_app())


@celery.task(name="tasks.add_together")
def add_together(a, b):
    return a + b


@celery.task(name="tasks.send_login_email")
def send_login_email(domain, user, email):

    subject = 'Hello, %s' % user
    html = '<p>Login <a target="_blank" href="%s">%s</a> Success</p>'
    msg = Message(
        sender='Walkerfree <407534636@qq.com>',
        subject=subject,
        html=html % (domain, domain),
        recipients=[email]
    )

    mail.send(msg)


@celery.task(name='tasks.find_pass_email')
def find_pass_email(domain, email, code):
    subject = 'Please verify your email address'
    html = '''
<html>
<body>
<p>Hi,</p>
<p style='padding-top: 10px;
    font-family: Helvetica,Helvetica neue,Arial,Verdana,sans-serif;
    color: #333333;
    font-size: 14px;
    line-height: 20px;
    text-align: left;'
>
Please reset your password, if it is not yours, ignore this!.</p>
<p>
<a
    href='%s'
    target='_blank'
    title='Verify link'
    style='font-size: 16px;
    font-family: Helvetica,Helvetica neue,Arial,Verdana,sans-serif;
    font-weight: none;
    color: #ffffff;
    text-decoration: none;
    background-color: #007bff;
    border-top: 11px solid #007bff;
    border-bottom: 11px solid #007bff;
    border-left: 20px solid #007bff;
    border-right: 20px solid #007bff;
    border-radius: 5px;
    display: inline-block;'
>Reset my password</a>
</p>
Or copy this link <b>%s</b> to reset your password.
</body>
</html>
'''
    link = '%s/auth/find/password/activate?code=%s'
    link = link % (
        domain,
        code
    )

    with mail.connect() as conn:

        msg = Message(
            sender='Walkerfree <407534636@qq.com>',
            subject=subject,
            html=html % (link, link),
            recipients=[email]
        )

        conn.send(msg)


@celery.task(name='tasks.send_register_email')
def send_register_email(domain, username, email, code):
    subject = 'Please verify your email address'
    html = '''
<html>
<body>
<p>Hi %s,</p>
<p style='padding-top: 10px;
    font-family: Helvetica,Helvetica neue,Arial,Verdana,sans-serif;
    color: #333333;
    font-size: 14px;
    line-height: 20px;
    text-align: left;'
>
Please verify your email address so we know that it's really you!.</p>
<p>
<a
    href='%s'
    target='_blank'
    title='Verify link'
    style='font-size: 16px;
    font-family: Helvetica,Helvetica neue,Arial,Verdana,sans-serif;
    font-weight: none;
    color: #ffffff;
    text-decoration: none;
    background-color: #007bff;
    border-top: 11px solid #007bff;
    border-bottom: 11px solid #007bff;
    border-left: 20px solid #007bff;
    border-right: 20px solid #007bff;
    border-radius: 5px;
    display: inline-block;'
>Verify my email address</a>
</p>
Or copy this link <b>%s</b> to verify your email.
</body>
</html>
'''
    link = '%s/auth/register/activate?code=%s' % (domain, code)

    with mail.connect() as conn:

        msg = Message(
            sender='Walkerfree <407534636@qq.com>',
            subject=subject,
            html=html % (username, link, link),
            recipients=[email]
        )

        conn.send(msg)
