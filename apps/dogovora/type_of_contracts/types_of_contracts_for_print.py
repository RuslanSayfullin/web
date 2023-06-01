# Типы договоров, по которым возможна печать
types_of_contracts_for_print = (
        'izgotovlenie_2021_02_mebeli',
        'mygkaya_2021_02_mebel',
        'technic_2021_04',
        'dveri',
        'izgotovlenie_mebeli',
        'mygkaya_mebel',
        'tehnika',
        'delivery',
        'izgotovlenie_2019_11_mebeli',
        'izgotovlenie_2020_09_mebeli',
        'mygkaya_2019_11_mebel',
        'mygkaya_2020_09_mebel',
        'tekstil_ip_sadykov_fiz',
        'tekstil_ip_usmanov_fiz',
        'montazh_demontazh_ip_sadykov_fiz',
        'iskusstvenny_kamen',
        'iskusstvenny_2021_02_kamen',
        'ekspress_dizayn',
        'podklyuchenie_2021_06_tehniki',
        'matrasy_2021_06',
        'carpets_and_rugs_ip',
        'decoration',
        'gotovaya_mebel_2021_06',
        'kuhonny_2021_07_garnitur_lite',
        'furniture_making',
        'upholstered_furniture',
        'mattresses_ooo-refabrik',
        'carpets_and_rugs_ooo-refabrik',
        'finishedfur_ooo-refabrik',
        'artificial_stone',
        'door_manufacturing',
        'transportation_services',
        'm_furniture_making',
        'm_upholstered_furniture',
        'm_mattresses',
        'm_householdtec',
        'm_connectiontec',
        'm_finishedfur',
        'm_doors',
        'm_stone',
        'm_textile',
        'm_transport',
        'm_assembling',
        'msk_textile_ip_sadykov',
        'msk_textile_ip_usmanov',
        'm_manufacturingassembling',
        'm_furnitureassemblywork',
        'm_2furnitureassemblywork',
        'entity_furniture_making',
        'juridical_moscow_ooo-refabrik_furniture_making',
        'entity_householdtec',
        'juridical_moscow_ooo-refabrik_householdtec',
        'entity_connectiontec',
        'entity_mattresses',
        'juridical_ooo-refabrik_mattresses',
        'entity_finishedfur',
        'juridical_ooo-refabrik_finishedfur',
        'entity_stone',
        'juridical_ooo-refabrik_stone',
        'entity_textile',
        'juridical_moscow_ooo-refabrik_textile',
        'entity_transport',
        'entity_assembling',
        'entity_furnitureassemblywork',
        'juridical_moscow_ooo-refabrik_furnitureassemblywork',
        'entity_ufa_furniture_making',
        'entity_ufa_ooo-refabrik_furniture_making',
        'entity_ufa_householdtec',
        'entity_ufa_ooo-refabrik_householdtec',
        'entity_ufa_connectiontec',
        'entity_ufa_mattresses',
        'entity_ufa_ooo-refabrik_mattresses',
        'entity_ufa_carpets_and_rugs',
        'entity_ufa_finishedfur',
        'entity_ufa_ooo-refabrik_finishedfur',
        'entity_ufa_stone',
        'entity_ufa_ooo-refabrik_stone',
        'entity_ufa_textile',
        'entity_ufa_ooo-refabrik_textile',
        'entity_ufa_transport',
        'entity_ufa_assembling',
    )

# Типы договоров, физ. лица
types_of_contracts_for_individuals = (
        'izgotovlenie_2021_02_mebeli',
        'mygkaya_2021_02_mebel',
        'technic_2021_04',
        'podklyuchenie_2021_06_tehniki',
        'matrasy_2021_06',
        'carpets_and_rugs_ip',
        'decoration',
        'gotovaya_mebel_2021_06',
        'iskusstvenny_2021_02_kamen',
        'tekstil_ip_sadykov_fiz',
        'tekstil_ip_usmanov_fiz',
        'dveri',
        'delivery',
        'montazh_demontazh_ip_sadykov_fiz',
        'ekspress_dizayn',
        'furniture_making',
        'upholstered_furniture',
        'mattresses_ooo-refabrik',
        'carpets_and_rugs_ooo-refabrik',
        'finishedfur_ooo-refabrik',
        'artificial_stone',
        'door_manufacturing',
        'transportation_services',
        'm_furniture_making',
        'm_upholstered_furniture',
        'm_mattresses',
        'm_householdtec',
        'm_connectiontec',
        'm_finishedfur',
        'm_doors',
        'm_stone',
        'm_textile',
        'msk_textile_ip_sadykov',
        'msk_textile_ip_usmanov',
        'm_transport',
        'm_assembling',
        'm_manufacturingassembling',
        'm_furnitureassemblywork',
        'm_2furnitureassemblywork'
)

# Типы договоров, для которых нужно заполнить товарный чек
types_of_contracts_with_sales_receipt = ('tehnika', 'technic_2021_04', 'matrasy_2021_06', 'carpets_and_rugs_ip',
                                         'carpets_and_rugs_ooo-refabrik',
                                         'decoration', 'gotovaya_mebel_2021_06', 'finishedfur_ooo-refabrik',
                                         'mattresses_ooo-refabrik', 'm_mattresses',
                                         'm_householdtec', 'm_finishedfur', 'entity_householdtec',
                                         'juridical_moscow_ooo-refabrik_householdtec',
                                         'entity_mattresses', 'juridical_ooo-refabrik_mattresses',
                                         'entity_finishedfur', 'juridical_ooo-refabrik_finishedfur',
                                         'entity_ufa_householdtec', 'entity_ufa_ooo-refabrik_householdtec',
                                         'entity_ufa_mattresses', 'entity_ufa_ooo-refabrik_mattresses',
                                         'entity_ufa_carpets_and_rugs',
                                         'entity_ufa_finishedfur', 'entity_ufa_ooo-refabrik_finishedfur')

# Типы договоров, которые можно привязать к другим договорам
connect_with_other_contract = ('technic_2021_04', 'matrasy_2021_06', 'carpets_and_rugs_ip',
                                'carpets_and_rugs_ooo-refabrik', 'mattresses_ooo-refabrik', 'm_mattresses',
                                'm_householdtec', 'entity_householdtec',
                                'juridical_moscow_ooo-refabrik_householdtec',
                                'entity_mattresses', 'juridical_ooo-refabrik_mattresses',
                                'entity_ufa_householdtec',
                                'entity_ufa_ooo-refabrik_householdtec', 'entity_ufa_mattresses',
                                'entity_ufa_ooo-refabrik_mattresses', 'entity_ufa_carpets_and_rugs')