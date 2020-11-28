# Cari hesap için farklı dillerde olan seçenekler yazılır

__supported_languages__ = ('TR', 'EN-EN', 'EN-US')

from checkaccount.errors import NoLangSpecified


class SystemProperties:
    lang = 'TR'  # default value

    @classmethod
    def change_lang(cls, value):
        if value not in __supported_languages__:
            raise NoLangSpecified()

        cls.lang = value


class CariHesapSpecs(SystemProperties):
    # sahis isletmesinde birthplace doldurulur.
    FIRM_TYPE_CHOICES = {'TR': (('t', 'TUZEL_KISILIK'), ('s', 'SAHIS_ISLETMESI')),
                         'EN-EN': (('l', 'LEGAL_ENTITIY'), ('s', 'SOLE_TRADER')),
                         'EN-US': (('l', 'LEGAL_ENTITIY'), ('s', 'SOLE_TRADER'))}
    IDENTITY_NUMBER_DIGIT = {'TR': 11,
                             'EN-US': 9,
                             'EN-EN': 11}

    TABLE_NAME = {'TR': 'CARI_HESAP',
                  'EN': 'CHECK_ACCOUNT'}

    key_contact_personnel = {'TR': 'FIRMA YETKILI KISISI', 'EN-EN': 'KEY CONTACT PERSONNEL',
                             'EN-US': 'KEY CONTACT PERSONNEL'}

    @classmethod
    def get_legal_entity(cls):
        return cls.get_firm_type_choices()[0][1]

    @classmethod
    def get_sole_trader(cls):
        return cls.get_firm_type_choices()[0][1]

    @classmethod
    def check_legal_entity(cls, value):
        if value == cls.get_legal_entity():
            return True
        else:
            return False

    @classmethod
    def get_key_contact_personnel(cls):
        return cls.key_contact_personnel[cls.lang]

    @classmethod
    def get_table_name(cls):
        return cls.TABLE_NAME[cls.lang]

    @classmethod
    def get_identity_digit_count(cls):
        return cls.IDENTITY_NUMBER_DIGIT[cls.lang]

    @classmethod
    def get_firm_type_choices(cls):
        return cls.FIRM_TYPE_CHOICES[cls.lang]

    # @classmethod
    # def get_sector_list(cls):
    #     return cls.SECTORS[cls.lang]


class AccountDocumentsSpec(SystemProperties):
    activity_certificate = {'verbose_name': {'TR': 'FAALIYET BELGESI',
                                             'EN-EN': 'ACTIVITY CERTIFICATE',
                                             'EN-US': 'ACTIVITY CERTIFICATE'},
                            }
    tax_return = {'verbose_name': {'TR': 'VERGI BEYANNAMESI',
                                   'EN-EN': 'TAX RETURN',
                                   'EN-US': 'TAX RETURN'}}

    authorized_signatures_list = {'verbose_name': {'TR': 'IMZA SIRKULERI',
                                                   'EN-EN': 'AUTHORIZED SIGNATURES LIST',
                                                   'EN-US': 'AUTHORIZED SIGNATURES LIST'}}

    @classmethod
    def get_tax_return_verbose_name(cls):
        return cls.tax_return['verbose_name'][cls.lang]

    @classmethod
    def get_activity_certificate_verbose_name(cls):
        return cls.activity_certificate['verbose_name'][cls.lang]

    @classmethod
    def get_authorized_signatures_list_verbose_name(cls):
        return cls.authorized_signatures_list['verbose_name'][cls.lang]


class PartnershipDocumentsSpecs(SystemProperties):
    partnership_structure_identity_copies = {'verbose_name': {'TR': 'ORTAKLIK YAPISI VE KIMLIK KOPYALARI',
                                                              'EN-EN': 'PARTNER STRUCTURE AND IDENTITY COPIES',
                                                              'EN-US': 'PARTNER STRUCTURE AND IDENTITY COPIES'}}

    identity_copies = {'verbose_name': {'TR': 'KIMLIK KOPYALARI',
                                        'EN-EN': 'IDENTITY COPIES',
                                        'EN-US': 'IDENTITY COPIES'}}

    board_structure = {'verbose_name': {'TR': 'YONETIM KURULU YAPISI',
                                        'EN-EN': 'BOARD MANAGEMENT',
                                        'EN-US': 'BOARD MANAGEMENT'}}

    @classmethod
    def get_partnership_structure_id_copies_verbose_name(cls):
        return cls.partnership_structure_identity_copies['verbose_name'][cls.lang]

    @classmethod
    def get_identity_copies_verbose_name(cls):
        return cls.identity_copies['verbose_name'][cls.lang]

    @classmethod
    def get_board_structure_verbose_name(cls):
        return cls.board_structure['verbose_name'][cls.lang]


