from django.db import connections

from isapilib.api.models import UserAPI, SepaCurrentVersion, SepaCompanies, SepaBranch, ApiLogs, SepaBranchUsers


def conn_production(fun):
    def wrapper_fun(*args, **kwargs):
        if 'production' not in connections.databases:
            production_database = connections.databases['default']
            production_database['NAME'] = production_database['NAME'].replace('test_', '')
            connections.databases['production'] = production_database
        return fun(*args, **kwargs)

    return wrapper_fun


@conn_production
def get_user(username, password, branch_pk) -> tuple[UserAPI, SepaBranch]:
    current_version = SepaCurrentVersion.objects.create()

    company = SepaCompanies.objects.create(
        id_intelisis=0,
    )

    production_branch = SepaBranch.objects.using('production').get(pk=branch_pk)

    branch = SepaBranch.objects.create(
        id_company=company,
        conf_ip_ext=production_branch.conf_ip_ext,
        conf_ip_int=production_branch.conf_ip_int,
        conf_user=production_branch.conf_user,
        conf_pass=production_branch.conf_pass,
        conf_db=production_branch.conf_db,
        conf_port=production_branch.conf_port,
        id_intelisis=production_branch.id_intelisis,
    )

    user = UserAPI.objects.create_user(
        id_branch=branch.pk,
        id_current_version=current_version.pk,
        code_verification='test',
        correo='test@test.test',
        telefono='1234567890',
        usuario=username,
        password=password,
    )

    SepaBranchUsers.objects.create(iduser=user, idbranch=branch)

    return user, branch


@conn_production
def get_logs(interfaz):
    return ApiLogs.objects.using('production').filter(interfaz=interfaz)
