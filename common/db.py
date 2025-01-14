#!/usr/bin/python
#encoding=gbk
###############
#访问数据库接口
#   提供功能:链接数据库执行sql语句；选取数据库记录，以tuple、dict、对象的形式返回
#
#
#   author: okicui
#   date  : 2012-11-22
###############

import re
import pickle
import sys
import MySQLdb
import pdb
import traceback
import time,datetime
from MySQLdb import escape_sequence
from MySQLdb.cursors import DictCursor
import _mysql_exceptions as MyExceptions
import logging
logger=logging.getLogger("dbRootLogger")

execfile('../conf/db.conf')

def get_caller(orgmode=False):
    """返回方法的调用者,输出日志时需要,方便调试"""
    import inspect
    stack=inspect.stack()[2]
    if orgmode:
        return "[[file:"+stack[1][stack[1].rfind('/')+1:]+"::"+str(stack[2])+"]] "+stack[3]
    else:
        return stack[1][stack[1].rfind('/')+1:]+":"+str(stack[2])+" "+stack[3]

class DBQuery(object):
    """数据库查询处理
       访问数据库封装类,提供各种访问数据库的方法
    """
    CURSOR_DICT = {}

    @staticmethod
    def get_conn(cursorcls=None):
        if cursorcls in DBQuery.CURSOR_DICT and DBQuery.CURSOR_DICT[cursorcls]:
            return DBQuery.CURSOR_DICT[cursorcls]
        """获取数据库连接
        cursorcls 为 MySQLdb.cursors.DictCursor时,查询结果将以字典的形式返回,数据库表的列名为key，数据库记录的值为value
        链接时 unix_socket需要设为/tmp/mysql.sock
        """

        mcdbDict = {
            'host'         : g_conf.DB_HOST,
            'user'         : g_conf.DB_USER,
            'passwd'       : g_conf.DB_PASSWORD,
            'db'           : g_conf.DB_DATABASE,
            'charset'      : g_conf.DB_CHARSET,
            'unix_socket'  : '/tmp/mysql.sock',
            'init_command' : "SET NAMES '%s';" % g_conf.DB_CHARSET
            }
        
        mcdbBakDict = {
            'host'         : g_conf.DB_HOST_BAK,
            'user'         : g_conf.DB_USER_BAK,
            'passwd'       : g_conf.DB_PASSWORD_BAK,
            'charset'      : g_conf.DB_CHARSET,
            'db'           : g_conf.DB_DATABASE_BAK,
            'unix_socket'  : '/tmp/mysql.sock',
            'init_command' : "SET NAMES '%s';"   % g_conf.DB_CHARSET
            }
        
        if cursorcls:
            mcdbBakDict['cursorclass']=cursorcls
            mcdbDict['cursorclass']=cursorcls
        
        conn = None
        for loop in range(0,10):        
            try:
                logger.debug("Before MySQLdb.connect")
                conn = MySQLdb.connect(**mcdbDict)
                logger.debug("After MySQLdb.connect")
                break
            except:
                logger.error('[链接数据库(主机)失败]:'+str(mcdbDict))
                logger.error(traceback.format_exc())
            time.sleep(1)

        if not conn:
            for loop in range(0,10):        
                try:
                    logger.debug("Before MySQLdb.connect bak")
                    conn = MySQLdb.connect(**mcdbBakDict)
                    logger.debug("After MySQLdb.connect bak")
                    break
                except:
                    logger.error('[链接数据库(备机)失败]:'+str(mcdbDict))
                    logger.error(traceback.format_exc())
                time.sleep(1)
        if conn:
            DBQuery.CURSOR_DICT[cursorcls] = conn
            return conn
        ##主备数据库都不能连接时报警
        alarm("[严重]无法连接任何数据库",dead=True , alarm_level=g_conf.ALARM_LEVEL_SERVER_CONDB_FAIL)


    @staticmethod
    def execute_sql(sql):
        """执行一条sql语句
        返回受影响的记录数；执行失败或发生异常返回-1
        """
        
        conn=DBQuery.get_conn()        
        cur=conn.cursor()
        affect = -1
        try:
            logger.debug('[DB] '+get_caller()+' \nsql='+sql)
            affect = cur.execute(sql)
            logger.debug('[DB] affect=%d'%(affect))                
            conn.commit()
        except:
            logger.error(traceback.format_exc())
            # 增加报警
            conn.rollback()  
        cur.close()
        #conn.close()
        return affect
    
    @staticmethod
    def executemany(sql, values):  
        conn = DBQuery.get_conn()
        cur = conn.cursor()
        affect = 0
        try:
            step = 10000
            for i in range((len(values) - 1)/step + 1):
                start = i * step
                end = (i + 1) * step
                #logger.debug( "[DB] "+get_caller()+" \nsql="+ sql % conn.literal(values[start:end]))
                affect += cur.executemany(sql, values[start:end])
                logger.debug('[DB] affect=%d'%(affect))
            conn.commit()
        except:
            logger.error(traceback.format_exc())
            conn.rollback()
        cur.close()
        return affect

    @staticmethod
    def insert_object(cls, object, columns=[]):
        objects = [object]
        return DBQuery.insert_objects[cls, objects, columns]

    @staticmethod
    def insert_objects(cls, objects, columns=[]):
        values = []
        if not columns:
            columns = cls.KEYS
        for  obj in objects:
            values.append(tuple([unicode(obj.__dict__[k]) for k in columns]))
        sql = 'INSERT INTO %s(%s) VALUES(%s)' % (cls.DB_TABLE, \
                ','.join(map(lambda s: '`%s`' % s, columns)), \
                ','.join(['%s'] * len(columns)))
        return DBQuery.executemany(sql, values)

    @staticmethod
    def execute_batch(sqls):
        """执行一批sql语句，返回是否改变数据库记录。"""
        changed=False
        conn=DBQuery.get_conn()        
        cur=conn.cursor()
        try:
            for sql in sqls:
                logger.debug('[DB] '+get_caller()+' \nsql='+sql)
                affect = cur.execute(sql)
                logger.debug('[DB] affect=%d'%(affect))                
            conn.commit()
            changed=True
        except:
            logger.error(traceback.format_exc())
            conn.rollback()  
        cur.close()
        #conn.close()
        return changed

    @staticmethod
    def get_dict(sql,params=[]):
        """#通过sql获取数据库记录的字典
        params 为 sql中 %s对应的参数对象
        #返回字典数组,key为 select 列名,value为其对应值

        如, get_dict('select * from client where id=%s and service=%s',[12,'cb'])

        """        
        conn=DBQuery.get_conn(MySQLdb.cursors.DictCursor)
        ##logger.debug( "[DB] sql="+sql)
        if params:
            logger.debug( "[DB] "+get_caller()+" \nsql="+ sql % conn.literal(params))
        else:
            logger.debug( "[DB] "+get_caller()+" \nsql="+ sql)
        try:
            cur = conn.cursor()
            ##执行查询
            if params:
                cur.execute(sql,params)
            else:
                cur.execute(sql)
            ##获取所有结果
            alldict=cur.fetchall()
            cur.close()
        except Exception,e:
            logger.error(traceback.format_exc())            
            alldict={}
        return alldict

    @staticmethod
    def get_tuple(sql,params=[]):
        """通过sql获取数据库表的tuple
        如, get_dict('select * from client where id=%s and service=%s',[12,'cb'])
        """        
        conn=DBQuery.get_conn()
        logger.debug( "[DB] "+get_caller()+" \nsql="+ sql % conn.literal(params))
        cur=conn.cursor()
        cur.execute(sql,params)
        alltuple=cur.fetchall()
        cur.close()
        #conn.close()
        return alltuple
    
    @staticmethod
    def get_table_dict(table,params=[],columns=[],**cond):
        """通过表名获取相应列字典
        columns 为列名(别名),如 ['id agentID',]   
        """
        if not columns:            
            sql = "SELECT * FROM "+table+" "
        else:
            #别名处理和escape列名
            cls=[]
            for s in columns:
                s=s.strip()
                if s.count(' ')==1:
                    cls.append("`"+s.replace(' ','` '))
                elif s.count(' ')==0:
                    cls.append("`"+s+"`")
                else:
                    raise Exception("too much space in column "+s)
            sql = "SELECT "+ ",".join(cls) + " FROM "+table
        
        ps=params[:]
        if cond:
            sql+=" WHERE "+" AND ".join(["`%s` = %%s" %(k) for k in cond.keys()])
            
        for k in cond.keys():
            ps.append(cond[k])

        return DBQuery.get_dict(sql,ps)
    
    @staticmethod
    def gen_insert_sql(cls, columns=[], values=[]):
        '''
        '''
        conn=DBQuery.get_conn()
        sql = 'INSERT INTO %s(%s) VALUES(%s)' % (cls.DB_TABLE, \
                ','.join(map(lambda s: '`%s`' % s, columns)), \
                ','.join(map(lambda s: '%s' % s, conn.literal(values))))
        return sql

    @staticmethod
    def gen_delete_sql(cls,**cond):        
        conn=DBQuery.get_conn()
        sql = 'DELETE FROM %s' % cls.DB_TABLE
        assert cond
        if cond:
            sql += " WHERE "+" AND ".join(["`%s`=%%s" %(k) for k in cond.keys()])
        params = []
        for k in cond.keys():
            params.append(cond[k])
        sql = sql % conn.literal(params)
        return sql
    
    @staticmethod
    def gen_update_sql(cls,columns=[],values=[],**cond):        
        """为更新对象的属性生成sql语句
        如,DBQuery.gen_update_sql(Client,['service_or_task'],[DBC.STATUS_TASK],id=123)
        将返回更新client表service_or_task列，值为TASK,条件为id=123
        即: update client set service_or_task=TASK wher id=123
        """
        conn=DBQuery.get_conn()
        if not columns or not values or len(columns)!=len(values):
            return '-1'
        params = values[:]
        sql = "UPDATE "+ cls.DB_TABLE+" SET " + ",".join(map(lambda s : "`"+s+"`=%s ",columns))        
        if cond:
            sql+=" WHERE "+" AND ".join(["`%s`=%%s" %(k) for k in cond.keys()])
        
        for k in cond.keys():
            params.append(cond[k])
        sql = sql % conn.literal(params)
        #conn.close()
        return sql
    
    @staticmethod
    def update_object(cls,columns=[],values=[],**cond):
        """更新cls对应的表
        如,DBQuery.update_object(Taskdef , ['status','end_time'],[DBC.STATUS_ERR,nowTime()],id=self.id)
        将taskdef表中的status,end_time更新为ERR,现在时间，条件时id=1
        """
        conn=DBQuery.get_conn()
        
        if not columns or not values or len(columns)!=len(values):
            return -1
        params=values[:]

        sql = "UPDATE "+cls.DB_TABLE+" SET " + ",".join(map(lambda s : "`"+s+"`=%s ",columns))
        
        if cond:
            sql+=" WHERE "+" AND ".join(["`%s` = %%s" %(k) for k in cond.keys()])
        
        for k in cond.keys():
            params.append(cond[k])

        logger.debug( "[DB] "+get_caller()+" \nsql="+ sql % conn.literal(params) )
        #pdb.set_trace()
        try:
            cur=conn.cursor()
            affect=cur.execute(sql,params)            
            conn.commit()
        except:
            logger.error(traceback.format_exc())
            print traceback.format_exc()
            conn.rollback()
        cur.close()
        #conn.close()
        return affect

    @staticmethod
    def load_objects_by_sql(cls,sql):
        """根据条件cond选取对象,把数据库得到每列加入到对象的属性中
        可以用列名进行属性访问，如 agent.id 将会是数据库id列对应的值
        如果columns为None，则将选出所有列
        coloumns可以为('col alias','col2 alias2')...
        """
        dbObs=DBQuery.get_dict(sql)        
        objs=[]
        for o in dbObs:
            obj=cls()
            for k,v in o.items():                
                obj.__setattr__(k,v)
            objs.append(obj)
        return objs
        
    @staticmethod
    def load_objects(cls,columns=[],**cond):
        """根据条件cond选取对象,把数据库得到每列加入到对象的属性中
        可以用列名进行属性访问，如 agent.id 将会是数据库id列对应的值
        如果columns为None，则将选出所有列
        coloumns可以为('col alias','col2 alias2')...
        """
        #logger.debug("columns="+str(columns))
        #logger.debug("cond="+ str( cond))
        if not columns:
            sql = "SELECT * FROM  %s" % cls.DB_TABLE
        else:
            sql = "SELECT %s FROM  %s" %  (",".join(columns),cls.DB_TABLE)
    
        params=[]
        if cond:
            sql+=" WHERE "+" AND ".join(["`%s` = %%s" %(k) for k in cond.keys()])
        
        
        for k in cond.keys():
            params.append(cond[k])
        #sql += ' limit 10' 
        dbObs=DBQuery.get_dict(sql,params)        
        objs=[]
        for o in dbObs:
            obj=cls()
            for k,v in o.items():                
                obj.__setattr__(k,v)
            objs.append(obj)
        return objs

    @staticmethod
    def load_object_by_id(cls,id,columns=[]):
        """通过主键获取对象"""
        cond={str(cls.PRIMARY_KEY):id}
        objs = DBQuery.load_objects(cls,columns,**cond) 
        if len(objs)==0:
            #raise Exception("no record in table "+cls.DB_TABLE+" "+cls.PRIMARY_KEY+"="+pkid)
            return None
        elif len(objs)>1:
            raise Exception(str(len(objs))+" records in table "+cls.DB_TABLE+" "+cls.PRIMARY_KEY+"="+id)            
        else:
            return objs[0]
