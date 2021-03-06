'''
Created on Dec 15, 2011

@author: shengb
'''
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import sqlite3

from pymasarsqlite.utils import checkConnection
from pymasarsqlite.service.service import (retrieveServices)
from pymasarsqlite.pvgroup.pvgroup import (retrievePvGroups)

def saveServiceConfig(conn, servicename, configname, configdesc=None, configversion=None, system=None, status="active"):
    """
    Link config attributes like name, description, ... with a given service name.
    The service config name for each different service has to be unique.
    By default, version for a new configuration is set to be 1, which means active.
    
    >>> import sqlite3
    >>> from pymasarsqlite.service.service import (saveService, retrieveServices)
    >>> from pymasarsqlite.db.masarsqlite import (SQL)
    >>> conn = sqlite3.connect(":memory:")
    >>> cur = conn.cursor()
    >>> result = cur.executescript(SQL)
    >>> saveService(conn, 'masar1', desc='non-empty description')
    1
    >>> saveService(conn, 'masar2', desc='non-empty description')
    2
    >>> saveServiceConfig(conn, 'masar1', 'orbit C01-C03', 'BPM horizontal readout for storage ring')
    1
    >>> #saveServiceConfig(conn, 'masar1', 'orbit C01-C03', 'BPM horizontal readout for storage ring')
    >>> saveServiceConfig(conn, 'masar2', 'orbit C01-C03', 'BPM horizontal readout for storage ring')
    2
    >>> saveServiceConfig(conn, 'masar2', 'RF', 'Storage ring RF system snapshot', system='SR')
    3
    >>> conn.close()
    """
    if configname is None:
        raise Exception('Service config name is not given')
        sys.exit()
    if status not in ["active", "inactive"]:
        raise ValueError("Service status has to be either active, or inactive")
    checkConnection(conn)
    serviceid = retrieveServices(conn, servicename)
    
    if len(serviceid) == 0:
        raise Exception('''service with given name ({0}) does not exist.'''.format(servicename))
        sys.exit()
    else:
        serviceid = serviceid[0][0]
    
    serviceconfigid = None
    try:
        cur = conn.cursor()
        
        cur.execute('select service_config_id from service_config where service_config_name = ? and service_id = ?', (configname, serviceid,))
        result = cur.fetchone()
        if result is None:            
            sql = 'insert into service_config (service_config_id, service_id, service_config_name, service_config_create_date, service_config_status '
            if configdesc is None and configversion is None:
                sql = sql + ') values(?,?,?,datetime("now"), ?)'
                cur.execute(sql, (None, serviceid, configname, status))
            elif configversion is None:
                sql = sql + ' , service_config_desc ) values(?,?,?,datetime("now"),?,?)'
                cur.execute(sql, (None,serviceid,configname, status,configdesc,))
            else:
                sql = sql + ' , service_config_desc, service_config_version ) values(?,?,?,datetime("now"),?, ?,?)'
                cur.execute(sql, (None,serviceid,configname,status,configdesc,configversion,))
            serviceconfigid = cur.lastrowid
            __saveConfigProp(cur, serviceconfigid, system)
        else:
            # @todo:  identify service config with given name exist already?
            serviceconfigid = result[0]
            raise Exception('service config exists already.')

#        cur.execute('select service_config_id from service_config where service_id = ?',(serviceid,))
#        print (cur.fetchall())
    except sqlite3.Error, e:
        print ("Error %s:" % e.args[0])
        raise
        sys.exit(1)
    
    return serviceconfigid

def __saveConfigProp (cur, serviceconfigid, system):
    if system is not None:
        sql = '''
        insert into service_config_prop (service_config_prop_id, service_config_id, service_config_prop_name, service_config_prop_value)
        values (?, ?, 'system', ?)
        '''
        try:
            # check this entity exists or not.
            cur.execute('select service_config_prop_id from service_config_prop where service_config_id = ? and service_config_prop_name = ? and service_config_prop_value = ?',
                        (serviceconfigid, 'system', system, ))
            result = cur.fetchone()
            if result is None:
                cur.execute(sql, (None, serviceconfigid, system,))
        except sqlite3.Error, e:
            print ('Error %s' %e.args[0])
            raise

def updateServiceConfigStatus(conn, configid, status="active"):
    """Update status of given configuration
    """
    sql = '''
    UPDATE service_config
    SET service_config_status = ?
    WHERE service_config_id = ?
    '''
    if status not in ["active", "inactive"]:
        raise ValueError("Service status has to be either active, or inactive")
    try:
        cur = conn.cursor()
        cur.execute(sql, (status, configid,))
    except sqlite3.Error, e:
        print ("Error %s:" % e.args[0])
        raise

def retrieveServiceConfigs(conn, servicename=None, configname=None, configversion=None, system=None, eventid=None):
    """
    Retrieve service config attributes like name, description, ... with given service name.    
    If service config name is none, retrieve all configs belong to a service with a given service name.
    If service name is none, retrieve all configs in service_config table.
    It returns tuple list with [(service_config_id, service_config_name, service_config_desc, service_config_create_date, 
    service_config_version, and service_config_status)].
    
    >>> import sqlite3
    >>> from pymasarsqlite.service.service import (saveService, retrieveServices)
    >>> from pymasarsqlite.db.masarsqlite import (SQL)
    >>> conn = sqlite3.connect(":memory:")
    >>> cur = conn.cursor()
    >>> result = cur.executescript(SQL)
    >>> saveService(conn, 'masar1', desc='non-empty description')
    1
    >>> saveService(conn, 'masar2', desc='non-empty description')
    2
    >>> saveServiceConfig(conn, 'masar1', 'orbit C01', 'BPM horizontal readout for storage ring')
    1
    >>> saveServiceConfig(conn, 'masar1', 'orbit C02', 'BPM horizontal readout for storage ring')
    2
    >>> saveServiceConfig(conn, 'masar2', 'orbit C01', 'BPM horizontal readout for storage ring')
    3
    >>> saveServiceConfig(conn, 'masar2', 'orbit C02', 'BPM horizontal readout for storage ring')
    4
    >>> saveServiceConfig(conn, 'masar2', 'RF snapshot', 'Storage ring RF system snapshot', system='SR')
    5
    >>> result = retrieveServiceConfigs(conn)
    >>> print (result[1][0], result[1][1], result[1][5])
    1 orbit C01 masar1
    >>> print (result[2][0], result[2][1], result[2][5])
    2 orbit C02 masar1
    >>> print (result[3][0], result[3][1], result[3][5])
    3 orbit C01 masar2
    >>> print (result[4][0], result[4][1], result[4][5])
    4 orbit C02 masar2
    >>> result = retrieveServiceConfigs(conn, servicename='masar1')
    >>> print (result[1][0], result[1][1])
    1 orbit C01
    >>> print (result[2][0], result[2][1])
    2 orbit C02
    >>> result = retrieveServiceConfigs(conn, configname='orbit C01')
    >>> print (result[1][0], result[1][1], result[1][5])
    1 orbit C01 masar1
    >>> print (result[2][0], result[2][1], result[2][5])
    3 orbit C01 masar2
    >>> result = retrieveServiceConfigs(conn, servicename='masar1', configname='orbit C01')
    >>> print (result[1][0], result[1][1])
    1 orbit C01
    >>> result = retrieveServiceConfigs(conn, system='SR1')
    >>> result = retrieveServiceConfigs(conn, system='SR')
    >>> print (result[1][0], ',', result[1][1], ',', result[1][2], ',', result[1][5])
    5 , RF snapshot , Storage ring RF system snapshot , masar2
    >>> result = retrieveServiceConfigs(conn, configname='RF snapshot', system='SR')
    >>> print (result[1][0], ',', result[1][1], ',', result[1][2], ',', result[1][5])
    5 , RF snapshot , Storage ring RF system snapshot , masar2
    >>> result = retrieveServiceConfigs(conn, servicename='masar2', system='SR')
    >>> print (result[1][0], ',', result[1][1], ',', result[1][2], ',', result[1][5])
    5 , RF snapshot , Storage ring RF system snapshot , masar2
    >>> result = retrieveServiceConfigs(conn, servicename='masar2', configname='RF snapshot', system='SR')
    >>> print (result[1][0], ',', result[1][1], ',', result[1][2], ',', result[1][5])
    5 , RF snapshot , Storage ring RF system snapshot , masar2
    >>> result = retrieveServiceConfigs(conn, system='SR1')
    >>> print (result)
    [(u'service_config_id', u'service_config_name', u'service_config_desc', u'service_config_create_date', u'service_config_version', u'service_name')]
    >>> conn.close()
    """

    checkConnection(conn)
    
    sql = '''
    select service_config.service_config_id, service_config_name, service_config_desc, service_config_create_date,
    service_config_version, service_config_status
    from service_config '''
    results = None
    if eventid is not None:
        sql += ' left join service_event using (service_config_id) where service_event_id = ?'
        cur = conn.cursor()
        cur.execute(sql, (eventid,))
        results = cur.fetchall()
    else:
        if configname != None:
            configname = configname.replace("*","%").replace("?","_")
        try:
            cur = conn.cursor()
            join = False
            if system is not None:
                join = True
                joinsql = ' left join service_config_prop using (service_config_id) '

            if configname is None and servicename is None:
                if join:
                    sql = sql + joinsql + ' where (service_config_prop_name = "system" and service_config_prop_value like ?) '
                    cur.execute(sql, (system,))
                else:
                    cur.execute(sql)
            elif servicename is None:
                if join:
                    sql = sql + joinsql + ' where service_config_name like ? and '
                    sql = sql + ' service_config_prop_name = "system" and service_config_prop_value like ? '
                    cur.execute(sql, (configname, system, ))
                else:
                    sql = sql + ' where service_config_name like ?'
                    cur.execute(sql, (configname,))
            elif configname is None:
                if join:
                    sql = sql + joinsql  + ' left join service using (service_id) where service.service_name = ? and '
                    sql += ' service_config_prop_name = "system" and service_config_prop_value like ? '
                    cur.execute(sql, (servicename, system))
                else:
                    sql = sql + ' , service where service_config.service_id = service.service_id and service.service_name = ?'
                    cur.execute(sql, (servicename,))
            else:
                if join:
                    sql = sql + joinsql + ' left join service using (service_id) '
                    sql = sql + ' where service_config_name like ? and service.service_name = ? and '
                    sql += ' (service_config_prop_name = "system" and service_config_prop_value like ?) '
    #                print (sql)
                    cur.execute(sql, (configname, servicename, system,))
                else:
                    sql = sql + ', service where service_config.service_id = service.service_id and service_config_name like ? and service.service_name = ?'
                    cur.execute(sql, (configname, servicename, ))
            results = cur.fetchall()
        except:
            raise
    results = [('config_idx', 'config_name', 'config_desc', 'config_create_date', 'config_version', 'status'), ] + results[:]
    return results

def saveServicePvGroup(conn, configname, pvgroups):
    """
    Assign pv groups to to a service config.
    
    >>> import sqlite3
    >>> conn = sqlite3.connect(':memory:')
    >>> from pymasarsqlite.service.service import (saveService, retrieveServices)
    >>> from pymasarsqlite.service.serviceconfig import(saveServicePvGroup, retrieveServicePvGroups)
    >>> from pymasarsqlite.pvgroup.pvgroup import (savePvGroup, retrievePvGroups)
    >>> from pymasarsqlite.db.masarsqlite import (SQL)
    >>> cur = conn.cursor()
    >>> result = cur.executescript(SQL)
    >>> serviceName1 = 'masar'
    >>> serviceDesc1 = 'masar service description example'
    >>> saveService(conn, serviceName1, serviceDesc1)
    1
    >>> serviceName2 = 'model'
    >>> serviceDesc2 = 'model service description example'
    >>> saveService(conn, serviceName2, serviceDesc2)
    2
    >>> masarconf1 = 'orbit C01'
    >>> masardesc1 = 'BPM horizontal readout for storage ring C01'
    >>> masarconf2 = 'orbit C02'
    >>> masardesc2 = 'BPM horizontal readout for storage ring C02'
    >>> saveServiceConfig(conn, serviceName1, masarconf1, masardesc1)
    1
    >>> saveServiceConfig(conn, serviceName1, masarconf2, masardesc2)
    2
    >>> modelconf1 = 'model conf 1'
    >>> modeldesc1 = 'model conf desc 1'
    >>> modelconf2 = 'model conf 2'
    >>> modeldesc2 = 'model conf desc 2'
    >>> saveServiceConfig(conn, serviceName2, modelconf1, modeldesc1)
    3
    >>> saveServiceConfig(conn, serviceName2, modelconf2, modeldesc2)
    4
    >>> result = retrieveServiceConfigs(conn, servicename='masar', configname='orbit C01')
    >>> pvgname1 = 'masar1group'
    >>> pvgdesc1 = 'this is my first pv group for masar service'
    >>> savePvGroup(conn, pvgname1, func=pvgdesc1)
    [1]
    >>> pvgname2 = 'masar2group'
    >>> pvgdesc2 = 'this is my new pv group for masar service with same group name'
    >>> savePvGroup(conn, pvgname2, func=pvgdesc2)
    [2]
    >>> pvgroups = retrievePvGroups(conn)
    >>> for pvgroup in pvgroups:
    ...    print (pvgroup[0], pvgroup[1])
    1 masar1group
    2 masar2group
    >>> pvgroups = retrievePvGroups(conn, pvgname1)
    >>> for pvgroup in pvgroups:
    ...    print (pvgroup[0], pvgroup[1])
    1 masar1group
    >>> pvgroups = retrievePvGroups(conn, pvgname2)
    >>> for pvgroup in pvgroups:
    ...    print (pvgroup[0], pvgroup[1])
    2 masar2group
    >>> saveServicePvGroup(conn, masarconf1, [pvgname1, pvgname2])
    [1, 2]
    >>> conn.close()
    """
    if configname is None or len(pvgroups) == 0:
        raise Exception('service config name or service name is empty.')
    checkConnection(conn)
    
    # get service config id
    serviceconfigid = retrieveServiceConfigs(conn, configname=configname)[1][0]
    pvg_serviceconfig_ids = []
    pvg_ids = []
    for pvgroup in pvgroups:
        pvg_id = retrievePvGroups(conn, pvgroup)
        if len(pvg_id) > 0:
            pvg_ids.append(retrievePvGroups(conn, pvgroup)[0][0])
        else:
            print ('given pv group name (%s) does not exist.' %pvgroup)
            raise Exception('given pv group name (%s) does not exist.' %pvgroup)
    try:
        cur = conn.cursor()
        sql = 'select pvgroup__serviceconfig_id from pvgroup__serviceconfig where service_config_id = ?'
        cur.execute(sql, (serviceconfigid,))
        result = cur.fetchone()
        
        if result is None:
            sql = 'insert into pvgroup__serviceconfig (pvgroup__serviceconfig_id, pv_group_id, service_config_id) values (?,?,?)'
            for pvg_id in pvg_ids:
                cur.execute(sql, (None, pvg_id, serviceconfigid))
                pvg_serviceconfig_ids.append(cur.lastrowid)
        else:
            #pvg_serviceconfig_ids = pvg_serviceconfig_ids[0]
            raise Exception('Service config has associated pv groups already.')
    except sqlite3.Error, e:
        print ('Error %s', e.arg[0])
        raise
    return pvg_serviceconfig_ids

def retrieveServicePvGroups(conn, configname, servicename=None):
    """
    Retrieve pv group names belonging to a given service config name.
    Return a tuple array with format [(pv_group_id, pv_group_name, service_config_name, service_name)].
    
    >>> import sqlite3
    >>> conn = sqlite3.connect(':memory:')
    >>> from pymasarsqlite.service.service import (saveService, retrieveServices)
    >>> from pymasarsqlite.service.serviceconfig import (saveServicePvGroup, retrieveServicePvGroups)
    >>> from pymasarsqlite.pvgroup.pvgroup import (savePvGroup, retrievePvGroups)
    >>> from pymasarsqlite.db.masarsqlite import SQL
    >>> cur = conn.cursor()
    >>> result = cur.executescript(SQL)
    >>> serviceName1 = 'masar'
    >>> serviceDesc1 = 'masar service description example'
    >>> saveService(conn, serviceName1, serviceDesc1)
    1
    >>> serviceName2 = 'model'
    >>> serviceDesc2 = 'model service description example'
    >>> saveService(conn, serviceName2, serviceDesc2)
    2
    >>> masarconf1 = 'orbit C01'
    >>> masardesc1 = 'BPM horizontal readout for storage ring C01'
    >>> masarconf2 = 'orbit C02'
    >>> masardesc2 = 'BPM horizontal readout for storage ring C02'
    >>> saveServiceConfig(conn, serviceName1, masarconf1, masardesc1)
    1
    >>> saveServiceConfig(conn, serviceName1, masarconf2, masardesc2)
    2
    >>> modelconf1 = 'model conf 1'
    >>> modeldesc1 = 'model conf desc 1'
    >>> modelconf2 = 'model conf 2'
    >>> modeldesc2 = 'model conf desc 2'
    >>> saveServiceConfig(conn, serviceName2, modelconf1, modeldesc1)
    3
    >>> saveServiceConfig(conn, serviceName2, modelconf2, modeldesc2)
    4
    >>> result = retrieveServiceConfigs(conn, servicename='masar', configname='orbit C01')
    >>> pvgname1 = 'masar1group'
    >>> pvgdesc1 = 'this is my first pv group for masar service'
    >>> savePvGroup(conn, pvgname1, func=pvgdesc1)
    [1]
    >>> pvgname2 = 'masar2group'
    >>> pvgdesc2 = 'this is my new pv group for masar service with same group name'
    >>> savePvGroup(conn, pvgname2, func=pvgdesc2)
    [2]
    >>> pvgroups = retrievePvGroups(conn)
    >>> for pvgroup in pvgroups:
    ...    print (pvgroup[0], pvgroup[1])
    1 masar1group
    2 masar2group
    >>> pvgroups = retrievePvGroups(conn, pvgname1)
    >>> for pvgroup in pvgroups:
    ...    print (pvgroup[0], pvgroup[1])
    1 masar1group
    >>> pvgroups = retrievePvGroups(conn, pvgname2)
    >>> for pvgroup in pvgroups:
    ...    print (pvgroup[0], pvgroup[1])
    2 masar2group
    >>> saveServicePvGroup(conn, masarconf1, [pvgname1, pvgname2])
    [1, 2]
    >>> saveServicePvGroup(conn, masarconf2, [pvgname1, pvgname2])
    [3, 4]
    >>> saveServicePvGroup(conn, modelconf1, [pvgname1, pvgname2])
    [5, 6]
    >>> saveServicePvGroup(conn, modelconf2, [pvgname1, pvgname2])
    [7, 8]
    >>> retrieveServicePvGroups(conn, masarconf1)
    [(1, u'masar1group', u'orbit C01', u'masar'), (2, u'masar2group', u'orbit C01', u'masar')]
    >>> retrieveServicePvGroups(conn, masarconf2, serviceName1)
    [(1, u'masar1group', u'orbit C02', u'masar'), (2, u'masar2group', u'orbit C02', u'masar')]
    >>> retrieveServicePvGroups(conn, modelconf1)
    [(1, u'masar1group', u'model conf 1', u'model'), (2, u'masar2group', u'model conf 1', u'model')]
    >>> conn.close()
    """
    if configname is None:
        raise Exception('service config name is not specified')
        sys.exit()
    checkConnection(conn)
    
    sql = ''' select pv_group.pv_group_id, pv_group.pv_group_name, service_config.service_config_name, service.service_name 
    from pv_group
    left join pvgroup__serviceconfig using (pv_group_id)
    left join service_config using (service_config_id)
    left join service using (service_id)
    where service_config.service_config_name = ?'''
    results = None

    try:
        cur = conn.cursor()
        if servicename is None:
            cur.execute(sql, (configname, ))
        else:
            services = retrieveServices(conn, servicename)
            if len(services) == 0:
                raise Exception('Given service (%s) does not exist.' %servicename)
            else:
                sql = sql + ' and service_config.service_id = ?'
                cur.execute(sql, (configname, services[0][0]))
        results = cur.fetchall()
    except sqlite3.Error, e:
        print ("Error %s:" % e.args[0])
        raise
        sys.exit(1)
    # should include service name and service config name?
    return results

#    cursor = conn.cursor() 
#    cursor.execute(SQL)
#    queryResponse = cursor.fetchall()
#    servicePvGroupNames = []
#    for pvg in queryResponse:
#        servicePvGroupNames.append(''.join(pvg[0]))
#    SQLsetServiceFromServiceID = '''
#        select service_name from service, service_config
#        where service.service_id = service_config.service_id
#        and service_config_id = %s '''
#    SQL = SQLsetServiceFromServiceID % serviceConfigId  #stupid trick to get around passing 2 args via js
#    cursor.execute(SQL)
#    service = cursor.fetchone()[0]
#    SQLgetServiceConfigNameFromServiceID = '''
#        select service_config_name from service_config
#        where service_config_id = %s '''
#    SQL = SQLgetServiceConfigNameFromServiceID % serviceConfigId  #stupid trick to get around passing 2 args via js
#    cursor.execute(SQL)
#    serviceConfigName = cursor.fetchone()[0]
#    d = {'service':service,'serviceConfigName':serviceConfigName, 'servicePvGroupNames':servicePvGroupNames,}
#    return d
#
def retrieveServiceConfigPVs(conn, configname, servicename=None):
    """
    Retrieve pv list associated with given service config name.
    
    >>> import sqlite3
    >>> conn = sqlite3.connect(':memory:')
    >>> from pymasarsqlite.service.service import (saveService, retrieveServices)
    >>> from pymasarsqlite.service.serviceconfig import(saveServicePvGroup, retrieveServicePvGroups)
    >>> from pymasarsqlite.pvgroup.pvgroup import (savePvGroup, retrievePvGroups)
    >>> from pymasarsqlite.pvgroup.pv import (saveGroupPvs, retrieveGroupPvs)
    >>> from pymasarsqlite.db.masarsqlite import (SQL)
    >>> cur = conn.cursor()
    >>> result = cur.executescript(SQL)
    >>> c01pvs = ['SR:C01-BI:G02A<BPM:L1>Pos-X', 'SR:C01-BI:G02A<BPM:L2>Pos-X',
    ...        'SR:C01-BI:G04A<BPM:M1>Pos-X', 'SR:C01-BI:G04B<BPM:M1>Pos-X',
    ...        'SR:C01-BI:G06B<BPM:H1>Pos-X', 'SR:C01-BI:G06B<BPM:H2>Pos-X']
    >>> c02pvs = ['SR:C02-BI:G02A<BPM:H1>Pos-X', 'SR:C02-BI:G02A<BPM:H2>Pos-X',
    ...        'SR:C02-BI:G04A<BPM:M1>Pos-X', 'SR:C02-BI:G04B<BPM:M1>Pos-X',
    ...        'SR:C02-BI:G06B<BPM:L1>Pos-X', 'SR:C02-BI:G06B<BPM:L2>Pos-X']
    >>> c03pvs = ['SR:C03-BI:G02A<BPM:L1>Pos-X', 'SR:C03-BI:G02A<BPM:L2>Pos-X',
    ...        'SR:C03-BI:G04A<BPM:M1>Pos-X', 'SR:C03-BI:G04B<BPM:M1>Pos-X',
    ...        'SR:C03-BI:G06B<BPM:H1>Pos-X', 'SR:C03-BI:G06B<BPM:H2>Pos-X']
    >>> c01desc = ['Horizontal orbit from BPM at C01 G02 L1', 'Horizontal orbit from BPM at C01 G02 L2',
    ...          'Horizontal orbit from BPM at C01 G04 M1', 'Horizontal orbit from BPM at C01 G04 M1',
    ...          'Horizontal orbit from BPM at C01 G06 H1', 'Horizontal orbit from BPM at C01 G06 H2']
    >>> c02desc = ['Horizontal orbit from BPM at C02 G02 H1', 'Horizontal orbit from BPM at C02 G02 H2',
    ...          'Horizontal orbit from BPM at C02 G04 M1', 'Horizontal orbit from BPM at C02 G04 M1',
    ...          'Horizontal orbit from BPM at C02 G06 L1', 'Horizontal orbit from BPM at C01 G06 L2']
    >>> c03desc = ['Horizontal orbit from BPM at C03 G02 L1', 'Horizontal orbit from BPM at C03 G02 L2',
    ...          'Horizontal orbit from BPM at C03 G04 M1', 'Horizontal orbit from BPM at C03 G04 M1',
    ...          'Horizontal orbit from BPM at C03 G06 H1', 'Horizontal orbit from BPM at C03 G06 H2']
    >>> c123pvs = ['SR:C02-BI:G02A<BPM:H1>Pos-X', 'SR:C02-BI:G02A<BPM:H2>Pos-X',
    ...        'SR:C03-BI:G02A<BPM:L1>Pos-X', 'SR:C03-BI:G02A<BPM:L2>Pos-X',
    ...        'SR:C01-BI:G06B<BPM:H1>Pos-X', 'SR:C01-BI:G06B<BPM:H2>Pos-X']
    >>> pvgname1 = 'pvg1'
    >>> pvgdesc1 = 'this is my 1st pv group for masar service'
    >>> savePvGroup(conn, pvgname1, func=pvgdesc1)
    [1]
    >>> pvgname2 = 'pvg2'
    >>> pvgdesc2 = 'this is my 2nd pv group for masar service'
    >>> savePvGroup(conn, pvgname2, func=pvgdesc2)
    [2]
    >>> pvgname3 = 'pvg3'
    >>> pvgdesc3 = 'this is my 3rd pv group for masar service'
    >>> savePvGroup(conn, pvgname3, func=pvgdesc3)
    [3]
    >>> pvgname4 = 'pvg4'
    >>> pvgdesc4 = 'this is mixed pv group for masar service'
    >>> savePvGroup(conn, pvgname4, func=pvgdesc4)
    [4]
    >>> saveGroupPvs(conn, pvgname1, c01pvs)
    [1, 2, 3, 4, 5, 6]
    >>> saveGroupPvs(conn, pvgname2, c02pvs)
    [7, 8, 9, 10, 11, 12]
    >>> saveGroupPvs(conn, pvgname3, c03pvs)
    [13, 14, 15, 16, 17, 18]
    >>> saveGroupPvs(conn, pvgname4, c123pvs)
    [19, 20, 21, 22, 23, 24]
    >>> sername1 = 'masar'
    >>> serdesc1 = 'masar service description'
    >>> sername2 = 'snapshot'
    >>> serdesc2 = 'snapshot service description'
    >>> sername3 = 'restore'
    >>> serdesc3 = 'restore service description'
    >>> saveService(conn, sername1, desc=serdesc1)
    1
    >>> saveService(conn, sername2, desc=serdesc2)
    2
    >>> saveService(conn, sername3, desc=serdesc3)
    3
    >>> confname1 = 'masar1'
    >>> confdesc1 = 'masar1 desc'
    >>> confname2 = 'masar2'
    >>> confdesc2 = 'masar2 desc'
    >>> confname3 = 'masar3'
    >>> confdesc3 = 'masar3 desc'
    >>> saveServiceConfig(conn, sername1, confname1, configdesc=confdesc1)
    1
    >>> saveServiceConfig(conn, sername1, confname2, configdesc=confdesc2)
    2
    >>> saveServiceConfig(conn, sername2, confname2, configdesc=confdesc2)
    3
    >>> saveServiceConfig(conn, sername2, confname3, configdesc=confdesc3)
    4
    >>> saveServiceConfig(conn, sername3, confname3, configdesc=confdesc3)
    5
    >>> saveServicePvGroup(conn, confname1, [pvgname1, pvgname2])
    [1, 2]
    >>> saveServicePvGroup(conn, confname2, [pvgname1, pvgname2, pvgname3])
    [3, 4, 5]
    >>> saveServicePvGroup(conn, confname3, [pvgname3, pvgname4])
    [6, 7]
    >>> retrieveServiceConfigPVs(conn, confname1, servicename=sername1)
    [u'SR:C01-BI:G02A<BPM:L1>Pos-X', u'SR:C01-BI:G02A<BPM:L2>Pos-X', u'SR:C01-BI:G04A<BPM:M1>Pos-X', u'SR:C01-BI:G04B<BPM:M1>Pos-X', ...
    u'SR:C01-BI:G06B<BPM:H1>Pos-X', u'SR:C01-BI:G06B<BPM:H2>Pos-X', u'SR:C02-BI:G02A<BPM:H1>Pos-X', u'SR:C02-BI:G02A<BPM:H2>Pos-X', ...
    u'SR:C02-BI:G04A<BPM:M1>Pos-X', u'SR:C02-BI:G04B<BPM:M1>Pos-X', u'SR:C02-BI:G06B<BPM:L1>Pos-X', u'SR:C02-BI:G06B<BPM:L2>Pos-X']
    >>> retrieveServiceConfigPVs(conn, confname3, servicename=sername1)
    []
    >>> retrieveServiceConfigPVs(conn, confname1)
    [u'SR:C01-BI:G02A<BPM:L1>Pos-X', u'SR:C01-BI:G02A<BPM:L2>Pos-X', u'SR:C01-BI:G04A<BPM:M1>Pos-X', u'SR:C01-BI:G04B<BPM:M1>Pos-X', ...
    u'SR:C01-BI:G06B<BPM:H1>Pos-X', u'SR:C01-BI:G06B<BPM:H2>Pos-X', u'SR:C02-BI:G02A<BPM:H1>Pos-X', u'SR:C02-BI:G02A<BPM:H2>Pos-X', ...
    u'SR:C02-BI:G04A<BPM:M1>Pos-X', u'SR:C02-BI:G04B<BPM:M1>Pos-X', u'SR:C02-BI:G06B<BPM:L1>Pos-X', u'SR:C02-BI:G06B<BPM:L2>Pos-X']
    >>> retrieveServiceConfigPVs(conn, confname2)
    [u'SR:C01-BI:G02A<BPM:L1>Pos-X', u'SR:C01-BI:G02A<BPM:L2>Pos-X', u'SR:C01-BI:G04A<BPM:M1>Pos-X', u'SR:C01-BI:G04B<BPM:M1>Pos-X', ...
    u'SR:C01-BI:G06B<BPM:H1>Pos-X', u'SR:C01-BI:G06B<BPM:H2>Pos-X', u'SR:C02-BI:G02A<BPM:H1>Pos-X', u'SR:C02-BI:G02A<BPM:H2>Pos-X', ...
    u'SR:C02-BI:G04A<BPM:M1>Pos-X', u'SR:C02-BI:G04B<BPM:M1>Pos-X', u'SR:C02-BI:G06B<BPM:L1>Pos-X', u'SR:C02-BI:G06B<BPM:L2>Pos-X', ...
    u'SR:C03-BI:G02A<BPM:L1>Pos-X', u'SR:C03-BI:G02A<BPM:L2>Pos-X', u'SR:C03-BI:G04A<BPM:M1>Pos-X', u'SR:C03-BI:G04B<BPM:M1>Pos-X', ...
    u'SR:C03-BI:G06B<BPM:H1>Pos-X', u'SR:C03-BI:G06B<BPM:H2>Pos-X']
    >>> retrieveServiceConfigPVs(conn, confname3)
    [u'SR:C01-BI:G06B<BPM:H1>Pos-X', u'SR:C01-BI:G06B<BPM:H2>Pos-X', u'SR:C02-BI:G02A<BPM:H1>Pos-X', ...
    u'SR:C02-BI:G02A<BPM:H2>Pos-X', u'SR:C03-BI:G02A<BPM:L1>Pos-X', u'SR:C03-BI:G02A<BPM:L2>Pos-X', ...
    u'SR:C03-BI:G04A<BPM:M1>Pos-X', u'SR:C03-BI:G04B<BPM:M1>Pos-X', u'SR:C03-BI:G06B<BPM:H1>Pos-X', ...
    u'SR:C03-BI:G06B<BPM:H2>Pos-X']
    """
    if configname is None:
        raise Exception('service config name is not specified')
        sys.exit()

    checkConnection(conn)
    sql  = '''
    select pv_name, pv_id from pv
    left join pv__pvgroup using (pv_id)
    left join pv_group using (pv_group_id)
    left join pvgroup__serviceconfig using (pv_group_id)
    left join service_config using (service_config_id)
    where service_config.service_config_name = ? '''
    pvlist = {}
    try:
        cur = conn.cursor()
        if servicename is None:
            cur.execute(sql, (configname, ))
        else:
            services = retrieveServices(conn, servicename)
            if len(services) == 0:
                raise Exception('Given service (%s) does not exist.' %servicename)
            else:
                sql = sql + ' and service_config.service_id = ?'
                cur.execute(sql, (configname, services[0][0]))
        results = cur.fetchall()
        for result in results:
            pvlist[result[1]] = result[0]
    except sqlite3.Error, e:
        print ("Error %s" %e.arg[0])
        raise
    
    return pvlist.values()


### pvmeta  ##############################################################
#def retrieveGroupPvs(conn,pvGroup):
#    SQLgetPvsForPvGroup = '''
#        select pv_name from pv 
#        left join pv__pvgroup using (pv_id) 
#        left join pv_group using (pv_group_id)
#        where pv_group_name = '%s' '''
#    SQL = SQLgetPvsForPvGroup % pvGroup
#    cursor = conn.cursor() 
#    cursor.execute(SQL)
#    queryResponse = cursor.fetchall()
#    pvNames = []
#    for pvName in queryResponse:
#        pvNames.append(''.join(pvName[0]))
#    SQLgetPvGroupDesc = "select pv_group_func from pv_group where pv_group_name = '%s' "
#    SQL = SQLgetPvGroupDesc % pvGroup
#    cursor.execute(SQL)
#    pvGroupDesc = cursor.fetchone()[0]
#    d = {'pvNames':pvNames,'pvGroup':pvGroup,'pvGroupDesc':pvGroupDesc,}
#    return d

if __name__ == "__main__":
    import doctest
    doctest.testmod()
