/**
 * @file TCSegFunc.h
 *
 * @author jianzhu 
 *
 * @date   2007-09-25
 * 
 * ����˵��.
 *
 * �����˷ִ������ýӿ�
 *
 */

#ifndef TX_PECKER_TCSEGFUNC_H
#define TX_PECKER_TCSEGFUNC_H

#include "TCPub.h"

typedef void* HANDLE;  

/** 
 * @brief ��ʼ����Ѷ�ִ�ϵͳ�����طִ�������.
 *
 * @param lpszDataDirPath �ִʴʵ���ԴĿ¼
 * @return �Ƿ��ʼ���ɹ�
 */
bool TCInitSeg(const char* lpszDataDirPath);


/** 
 * @brief �����Զ����ķִʽ�����
 *
 * @param  iResultMode �ִʿ���
 * @return �ִʾ��
 */
HANDLE TCCreateSegHandle(int iResultMode);


/** 
 * @brief �ַ����Զ����ķִʺ���
 * 
 * @param hHandle   �ִʾ��
 * @param lpText    ���з��ı�
 * @param nTextLen  ���з��ı�����
 * @param nCharSet  �ַ�����
 * 
 * @return �Ƿ��зֳɹ�
 */
bool TCSegment(HANDLE hHandle, const char* lpText, size_t nTextLen = 0, size_t nCharSet = TC_GBK);


/** 
 * @brief �õ��ִʽ���еĴʵĸ���
 * @param hHandle �ִʾ��
 */
int  TCGetResultCnt(HANDLE hHandle);


/** 
 * @brief ��÷ִʽ����ָ��λ�õĴ�
 * 
 * @param hHandle �ִʾ��
 * @param index   �ʵ�λ��
 * 
 * @return �ִʽ���� index λ�õĴ�
 */
char* TCGetWordAt(HANDLE hHandle, int index);


/** 
 * @brief ��÷ִʽ����ָ��λ�õĴʺʹ���
 * 
 * @param hHandle �ִʾ��
 * @param index   �ʵ�λ��
 * 
 * @return �ִʽ���� index λ�õĴʺʹ���
 */
pWP TCGetAt(HANDLE hHandle, int index);

/** 
 * @brief ��÷ִʽ����ָ��λ�õĴ�(Multi-Seg)
 * 
 * @param hHandle �ִʾ��
 * @param index   �ʵ�λ��
 * 
 * @return �ִʽ���� index λ�õĴ�
 */
p_ms_word_t TCMSGetWordAt(HANDLE hHandle, int index);


/** 
 * @brief ��÷ִʽ����ָ��λ�õĴʺʹ���(Multi-Seg)
 * 
 * @param hHandle �ִʾ��
 * @param index   �ʵ�λ��
 * 
 * @return �ִʽ���� index λ�õĴʺʹ���
 */
p_ms_wp_t TCMSGetAt(HANDLE hHandle, int index);

/**
 * @brief ��ȡ���зִʽ��
 *
 * @param hHandle    �ִʾ��
 * @param seg_tokens ���зִʽ��
 *
 * @return ���зִʽ��������seg_tokens��
 */
void TCGetAllSegInfo(HANDLE hHandle, seg_tokens_t &seg_tokens);

/**
 * @brief �������ı����GBKת��Ϊutf8
 *
 * @param hHandle �ִʾ��
 * @param word ����
 * @param wlen �ʳ�
 */
void TCConvertWordCharsetToUTF8(HANDLE hHandle, const char *&word, size_t &wlen);

/** 
 * @brief  �رշִʾ��
 * 
 * @param hHandle �ִʾ��
 */
void TCCloseSegHandle(HANDLE hHandle);


/** 
 * @brief ж����Ѷ���ķִ�ϵͳ���ͷŷִ�ϵͳ��ռ��Դ
 */
void TCUnInitSeg(void);

/**
 * @brief ��ȡ�û��Զ���������
 *
 * @param hHandle �ִʾ��
 * @param cls     �û��Զ�����������
 *
 * @return ���ظ÷���Ŷ�Ӧ�ķ�����
 */
int TCGetClsNum(HANDLE hHandle, int cls);


/**
 * @brief ��ȡ�û��Զ���ʵ����
 *
 * @param hHandle �ִʾ��
 * @param cls     �û��Զ�����������
 * @param idx     Ҫ��ȡ���������
 *
 * @return ��������ָ�������
 */
const char* TCGetClsAt(HANDLE hHandle, int cls, int idx);



/**
 * @brief �趨�û��Զ����ƥ���,�ִ����ģʽ
 *
 * ʹ���û��Զ���󣬷ִ��������������ģʽ
 * OUT_WORD          ��ͨ�ִ����
 * OUT_PHRASE        �����Զ���������ƥ������
 * OUT_SUBPHRASE     ����ƥ��Ķ����б����
 *
 * @param hHandle     �ִʾ��
 * @param outMode     ���ȡ��ģʽ
 */
void TCSetOutMode(HANDLE hHandle, OutMode outMode);


/** 
 * @brief �л��û��û��Զ���ʵ�
 * 
 * @param sUserDict �û��Զ���ʵ�·��
 */
void TCChangeUserDict(const char* sUserDict);


/** 
 * @brief ��������ʾ�Ĵ���תΪ�ַ�����ʾ
 * 
 * @param idPos  [in]  ����Ĵ�������
 * @param strPos [out] �����Ӧ�Ĵ��Դ�
 */
void TCPosId2Str(int idPos, char* strPos);


/** 
 * @brief ʹ�� pku ģʽ��ʶ�� �����ڲ�����
 * @param hHandle �ִʾ��
 */
void TCSetPKUMode(HANDLE hHandle);


#endif /* TX_PECKER_TCSEGFUNC_H */
