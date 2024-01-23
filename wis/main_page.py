r"""!
\mainpage Wiseye

\section s Important Commands:

\subsection ss1 Building system:
docker-compose -f local.yml build

\subsection ss2 Running migrations:
docker-compose -f local.yml run –rm django manage.py migrate

\subsection ss3 Creating admin account:
docker-compose -f local.yml run –rm django manage.py createsuperuser

\subsection ss4 Run system (without build):
docker-compose -f local.yml up

"""
