USE sandra_db;

INSERT INTO warehouses (id, name, country, county, town, created_at, updated_at) VALUES
-- Nairobi County
(UUID(), 'house_nairobi_west', 'Kenya', 'Nairobi', 'Nairobi', NOW(), NOW()),
(UUID(), 'house_karen', 'Kenya', 'Nairobi', 'Nairobi', NOW(), NOW()),
(UUID(), 'house_ruaka', 'Kenya', 'Nairobi', 'Nairobi', NOW(), NOW()),
(UUID(), 'house_westlands', 'Kenya', 'Nairobi', 'Nairobi', NOW(), NOW()),
(UUID(), 'house_embakasi', 'Kenya', 'Nairobi', 'Nairobi', NOW(), NOW()),

-- Mombasa County
(UUID(), 'house_mombasa_island', 'Kenya', 'Mombasa', 'Mombasa', NOW(), NOW()),
(UUID(), 'house_nyali', 'Kenya', 'Mombasa', 'Mombasa', NOW(), NOW()),
(UUID(), 'house_bamburi', 'Kenya', 'Mombasa', 'Mombasa', NOW(), NOW()),
(UUID(), 'house_kisauni', 'Kenya', 'Mombasa', 'Mombasa', NOW(), NOW()),
(UUID(), 'house_mikindani', 'Kenya', 'Mombasa', 'Mombasa', NOW(), NOW()),

-- Kisumu County
(UUID(), 'house_kisumu_central', 'Kenya', 'Kisumu', 'Kisumu', NOW(), NOW()),
(UUID(), 'house_milimani', 'Kenya', 'Kisumu', 'Kisumu', NOW(), NOW()),
(UUID(), 'house_nyalenda', 'Kenya', 'Kisumu', 'Kisumu', NOW(), NOW()),
(UUID(), 'house_mamboleo', 'Kenya', 'Kisumu', 'Kisumu', NOW(), NOW()),
(UUID(), 'house_kondele', 'Kenya', 'Kisumu', 'Kisumu', NOW(), NOW()),

-- Nakuru County
(UUID(), 'house_nakuru_town', 'Kenya', 'Nakuru', 'Nakuru', NOW(), NOW()),
(UUID(), 'house_naivasha', 'Kenya', 'Nakuru', 'Naivasha', NOW(), NOW()),
(UUID(), 'house_rongai', 'Kenya', 'Nakuru', 'Rongai', NOW(), NOW()),
(UUID(), 'house_molo', 'Kenya', 'Nakuru', 'Molo', NOW(), NOW()),
(UUID(), 'house_nyahururu', 'Kenya', 'Nakuru', 'Nyahururu', NOW(), NOW()),

-- Uasin Gishu County
(UUID(), 'house_eldoret', 'Kenya', 'Uasin Gishu', 'Eldoret', NOW(), NOW()),
(UUID(), 'house_kipkaren', 'Kenya', 'Uasin Gishu', 'Eldoret', NOW(), NOW()),
(UUID(), 'house_ngata', 'Kenya', 'Uasin Gishu', 'Eldoret', NOW(), NOW()),
(UUID(), 'house_ziwa', 'Kenya', 'Uasin Gishu', 'Eldoret', NOW(), NOW()),
(UUID(), 'house_cheptiret', 'Kenya', 'Uasin Gishu', 'Eldoret', NOW(), NOW()),

-- Kiambu County
(UUID(), 'house_thika', 'Kenya', 'Kiambu', 'Thika', NOW(), NOW()),
(UUID(), 'house_kiambu_town', 'Kenya', 'Kiambu', 'Kiambu', NOW(), NOW()),
(UUID(), 'house_ruiru', 'Kenya', 'Kiambu', 'Ruiru', NOW(), NOW()),
(UUID(), 'house_githunguri', 'Kenya', 'Kiambu', 'Githunguri', NOW(), NOW()),
(UUID(), 'house_karuri', 'Kenya', 'Kiambu', 'Karuri', NOW(), NOW()),

-- Meru County
(UUID(), 'house_meru_town', 'Kenya', 'Meru', 'Meru', NOW(), NOW()),
(UUID(), 'house_maua', 'Kenya', 'Meru', 'Maua', NOW(), NOW()),
(UUID(), 'house_nkubu', 'Kenya', 'Meru', 'Nkubu', NOW(), NOW()),
(UUID(), 'house_timau', 'Kenya', 'Meru', 'Timau', NOW(), NOW()),
(UUID(), 'house_mikinduri', 'Kenya', 'Meru', 'Mikinduri', NOW(), NOW()),

-- Kakamega County
(UUID(), 'house_kakamega_town', 'Kenya', 'Kakamega', 'Kakamega', NOW(), NOW()),
(UUID(), 'house_mumias', 'Kenya', 'Kakamega', 'Mumias', NOW(), NOW()),
(UUID(), 'house_malava', 'Kenya', 'Kakamega', 'Malava', NOW(), NOW()),
(UUID(), 'house_navakholo', 'Kenya', 'Kakamega', 'Navakholo', NOW(), NOW()),
(UUID(), 'house_shinyalu', 'Kenya', 'Kakamega', 'Shinyalu', NOW(), NOW()),

-- Bungoma County
(UUID(), 'house_bungoma_town', 'Kenya', 'Bungoma', 'Bungoma', NOW(), NOW()),
(UUID(), 'house_webuye', 'Kenya', 'Bungoma', 'Webuye', NOW(), NOW()),
(UUID(), 'house_chwele', 'Kenya', 'Bungoma', 'Chwele', NOW(), NOW()),
(UUID(), 'house_kimilili', 'Kenya', 'Bungoma', 'Kimilili', NOW(), NOW()),
(UUID(), 'house_malakisi', 'Kenya', 'Bungoma', 'Malakisi', NOW(), NOW()),

-- Nyeri County
(UUID(), 'house_nyeri_town', 'Kenya', 'Nyeri', 'Nyeri', NOW(), NOW()),
(UUID(), 'house_karatina', 'Kenya', 'Nyeri', 'Karatina', NOW(), NOW()),
(UUID(), 'house_nyeri_hill', 'Kenya', 'Nyeri', 'Nyeri', NOW(), NOW()),
(UUID(), 'house_mathira', 'Kenya', 'Nyeri', 'Mathira', NOW(), NOW()),
(UUID(), 'house_oci', 'Kenya', 'Nyeri', 'Othaya', NOW(), NOW()),

-- Machakos County
(UUID(), 'house_machakos_town', 'Kenya', 'Machakos', 'Machakos', NOW(), NOW()),
(UUID(), 'house_athiriver', 'Kenya', 'Machakos', 'Athi River', NOW(), NOW()),
(UUID(), 'house_kangundo', 'Kenya', 'Machakos', 'Kangundo', NOW(), NOW()),
(UUID(), 'house_masii', 'Kenya', 'Machakos', 'Masii', NOW(), NOW()),
(UUID(), 'house_mutituni', 'Kenya', 'Machakos', 'Mutituni', NOW(), NOW()),

-- Kajiado County
(UUID(), 'house_kajiado_town', 'Kenya', 'Kajiado', 'Kajiado', NOW(), NOW()),
(UUID(), 'house_ngong', 'Kenya', 'Kajiado', 'Ngong', NOW(), NOW()),
(UUID(), 'house_kitengela', 'Kenya', 'Kajiado', 'Kitengela', NOW(), NOW()),
(UUID(), 'house_olooloitikoshi', 'Kenya', 'Kajiado', 'Olooloitikoshi', NOW(), NOW()),
(UUID(), 'house_isinya', 'Kenya', 'Kajiado', 'Isinya', NOW(), NOW()),

-- Kericho County
(UUID(), 'house_kericho_town', 'Kenya', 'Kericho', 'Kericho', NOW(), NOW()),
(UUID(), 'house_litein', 'Kenya', 'Kericho', 'Litein', NOW(), NOW()),
(UUID(), 'house_bureti', 'Kenya', 'Kericho', 'Bureti', NOW(), NOW()),
(UUID(), 'house_sosiot', 'Kenya', 'Kericho', 'Sosiot', NOW(), NOW()),
(UUID(), 'house_kipkelion', 'Kenya', 'Kericho', 'Kipkelion', NOW(), NOW()),

-- Kisii County
(UUID(), 'house_kisii_town', 'Kenya', 'Kisii', 'Kisii', NOW(), NOW()),
(UUID(), 'house_suneka', 'Kenya', 'Kisii', 'Suneka', NOW(), NOW()),
(UUID(), 'house_ogembo', 'Kenya', 'Kisii', 'Ogembo', NOW(), NOW()),
(UUID(), 'house_nyamache', 'Kenya', 'Kisii', 'Nyamache', NOW(), NOW()),
(UUID(), 'house_tabaka', 'Kenya', 'Kisii', 'Tabaka', NOW(), NOW()),

-- Kilifi County
(UUID(), 'house_kilifi_town', 'Kenya', 'Kilifi', 'Kilifi', NOW(), NOW()),
(UUID(), 'house_malindi', 'Kenya', 'Kilifi', 'Malindi', NOW(), NOW()),
(UUID(), 'house_mtwapa', 'Kenya', 'Kilifi', 'Mtwapa', NOW(), NOW()),
(UUID(), 'house_mariakani', 'Kenya', 'Kilifi', 'Mariakani', NOW(), NOW()),
(UUID(), 'house_tezo', 'Kenya', 'Kilifi', 'Tezo', NOW(), NOW()),

-- Nyandarua County
(UUID(), 'house_nyahururu', 'Kenya', 'Nyandarua', 'Nyahururu', NOW(), NOW()),
(UUID(), 'house_olkalou', 'Kenya', 'Nyandarua', 'Ol Kalou', NOW(), NOW()),
(UUID(), 'house_ndaragwa', 'Kenya', 'Nyandarua', 'Ndaragwa', NOW(), NOW()),
(UUID(), 'house_kinangop', 'Kenya', 'Nyandarua', 'Kinangop', NOW(), NOW()),
(UUID(), 'house_engineer', 'Kenya', 'Nyandarua', 'Engineer', NOW(), NOW()),

-- Trans Nzoia County
(UUID(), 'house_kitale', 'Kenya', 'Trans Nzoia', 'Kitale', NOW(), NOW()),
(UUID(), 'house_kwanza', 'Kenya', 'Trans Nzoia', 'Kwanza', NOW(), NOW()),
(UUID(), 'house_endebess', 'Kenya', 'Trans Nzoia', 'Endebess', NOW(), NOW()),
(UUID(), 'house_kimini', 'Kenya', 'Trans Nzoia', 'Kiminini', NOW(), NOW()),
(UUID(), 'house_sirende', 'Kenya', 'Trans Nzoia', 'Sirende', NOW(), NOW());