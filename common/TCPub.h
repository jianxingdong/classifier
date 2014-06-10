/**
 * @file TCPub.h
 *
 * @author jianzhu 
 *
 * @date   2007-09-25
 * 
 * ����˵��.
 *
 * �����˷ִ��������еĿ���
 *
 */

#ifndef TX_PECKER_TCPUB_H
#define TX_PECKER_TCPUB_H

#include <cstddef>

/////////////////////////////////////////////////////////////////////////////////////////////
//                        �µķִʽ����ȡ�ӿ�                                             //
/////////////////////////////////////////////////////////////////////////////////////////////
typedef struct _token_t
{
    const char      *word; // ����
    unsigned char   pos;   // ����
    size_t          wlen;  // �ʳ�
    unsigned char   wtype; // ����(0-��ͨ�� 1-multiseg��һ���з���ʽ 2-multiseg�ڶ����з���ʽ)
}token_t;

typedef struct _comb_token_t
{
    const char      *word; // ����
    unsigned char   pos;   // ����
    size_t          wlen;  // �ʳ�
    int             cls;   // ����� ������Ϣֻ���û��Զ���ʡ��������Ч��
    size_t          sidx;  // ��ϸ�з��п�ʼ������
    size_t          eidx;  // ��ϸ�з��н���������
}comb_token_t;

typedef struct _seg_tokens_t
{
    // ϸ�����зִ���
    token_t        *fine_grain_seg_tokens;
    size_t          fine_grain_tokens_num;
    
    // �������зִ���
    comb_token_t   *thick_seg_tokens;
    size_t          thick_seg_tokens_num;

    // �û��Զ�����зִ���
    comb_token_t   *custom_defined_tokens;
    size_t          custom_tokens_num;

    // �û��Զ�������зִ���
    comb_token_t   *custom_defined_phrases;
    size_t          custom_phrases_num;

    // ͬ��ʴ���
    comb_token_t   *synonym_tokens;
    size_t          synonym_tokens_num;
}seg_tokens_t;

//////////////////////////////////////////////////////////////////////////////////////////////
//                        �ɵķִʽ����ȡ�ӿ�                                              //
//////////////////////////////////////////////////////////////////////////////////////////////
// ���ڱ���ִʷ��ؽ���Ľṹ��
typedef struct wordpos
{
    const char* word;
    int         pos;
    bool        bcw;  // �û��Զ���� ? true : false
    int         cls;  // (�û��Զ���� && TC_CLS) ? �û��Զ���ʷ���� : NULL
}WP, *pWP;

// ���ڱ���multi-seg�ִʷ��ؽ���Ľṹ��
typedef struct
{
   char *word;
   int	idx;
}ms_word_t, *p_ms_word_t;

// ���ڱ���mult-seg�ִʴ��Ա�ע���ؽ���Ľṹ��
typedef struct
{
    const char* word;
    int         pos;
    bool        bcw;  // �û��Զ���� ? true : false
    int         cls;  // (�û��Զ���� && TC_CLS) ? �û��Զ���ʷ���� : NULL
    int         idx;
}ms_wp_t, *p_ms_wp_t;


///////////////////////////////////////////////////////////////////////////////////
//                ʹ���û��Զ���ʺ��ȡ�����ģʽ(default:OUT_WORD)             //
///////////////////////////////////////////////////////////////////////////////////
enum OutMode {
    OUT_WORD = 1,
    OUT_PHRASE,
    OUT_SUBPHRASE
};

////////////////////////////////////////////////////////////////////////////////////
//                             �ִ��зֿ���                                       //
////////////////////////////////////////////////////////////////////////////////////
// ����Ӣ�Ĵ�����ʱʹ��С����ģʽ�����ȼ�����TC_GU)
#define TC_ENGU             0x00000001

// �����ִ�ϵͳʹ��С����ģʽ
#define TC_GU               0x00000002

// ���д��Ա�ע
#define TC_POS              0x00000004

// ʹ���û��Զ����
#define TC_USR              0x00000008

// ����ȫ�ǰ��ת��
#define TC_S2D              0x00000010

// ����Ӣ�Ĵ�Сдת��
#define TC_U2L              0x00000020

// ��ע�û��Զ���ʷ����
#define TC_CLS              0x00000040

// ʹ�ù���
#define TC_RUL              0x00000080

// ʹ������ʶ��
#define TC_CN               0x00000100

// ʹ�÷���ת����
#define TC_T2S              0x00000200

// ����С���ȿ���
#define TC_PGU              0x00000400

// ����С��������
#define TC_LGU              0x00000800

// ����׺�ֵĴ�С���ȿ���
#define TC_SGU              0x00001000

// ����ģʽ�зֿ���
#define TC_CUT              0x00002000

// ƪ����Ϣ�ִʿ���
#define TC_TEXT             0x00004000

// �ַ������� ����ȫ���ת���رտ���
#define TC_CONV             0x00008000

// ������Ƭ�β���Multi-Seg
#define TC_WMUL             0x00010000

// ���������Ƭ�β���Multi-Seg
#define TC_PMUL             0x00020000

// ASCII�ַ�����Ϊ�����з�
#define TC_ASC              0x00040000

// ʹ�ö�������
#define TC_SECPOS           0x00080000

// �ַ��������ʽ
// GBK����
#define TC_GBK              0x00100000

// UTF-8����
#define TC_UTF8             0x00200000

// ���������µĽӿ���ʽ����ͬʱ����
// ϸ�з֡����з֡��û��Զ���ʡ�����ʡ�ͬ���
#define TC_NEW_RES          0x00400000

// ��������ͬ���
#define TC_SYN              0x00800000

// ����ʶ�𿪹�
#define TC_LN               0x01000000

// ������Ƭ�β���ϸ�з�
#define TC_WGU              0x02000000

///////////////////////////////////////////////////////////////////////////////////////////////////
//                            �ִʴ���                                                           //
///////////////////////////////////////////////////////////////////////////////////////////////////
#define TC_A    1   // ���ݴ�
#define TC_AD   2   // ���δ�
#define TC_AN   3   // ���δ�
#define TC_B    4   // �����
#define TC_C    5   // ����
#define TC_D    6   // ����
#define TC_E    7   // ̾��
#define TC_F    8   // ��λ��
#define TC_G    9   // ���ش�
#define TC_H    10  // ǰ�ӳɷ�
#define TC_I    11  // ����
#define TC_J    12  // �������
#define TC_K    13  // ��ӳɷ�
#define TC_L    14  // ϰ����
#define TC_M    15  // ����
#define TC_N    16  // ����
#define TC_NR   17  // ����
#define TC_NRF  18  // ��
#define TC_NRG  19  // ��
#define TC_NS   20  // ����
#define TC_NT   21  // ��������
#define TC_NZ   22  // ����ר��
#define TC_NX   23  // �Ǻ��ִ�
#define TC_O    24  // ������
#define TC_P    25  // ���
#define TC_Q    26  // ����
#define TC_R    27  // ����
#define TC_S    28  // ������
#define TC_T    29  // ʱ���
#define TC_U    30  // ����
#define TC_V    31  // ����
#define TC_VD   32  // ������
#define TC_VN   33  // ������
#define TC_W    34  // ������
#define TC_X    35  // ��������
#define TC_Y    36  // ������
#define TC_Z    37  // ״̬��
#define TC_AG   38  // ������
#define TC_BG   39  // ��������
#define TC_DG   40  // ������
#define TC_MG   41  // ����������
#define TC_NG   42  // ������
#define TC_QG   43  // ������
#define TC_RG   44  // ������
#define TC_TG   45  // ʱ����
#define TC_VG   46  // ������
#define TC_YG   47  // ����������
#define TC_ZG   48  // ״̬������
#define TC_SOS  49  // ��ʼ��
#define TC_EOS  55  // ������
#define TC_UNK  0   // δ֪����

#define TC_WWW      50  // URL
#define TC_TELE     51  // �绰����
#define TC_EMAIL    52  // email

#endif /* TX_PECKER_TCPUB_H */
