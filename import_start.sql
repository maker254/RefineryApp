INSERT INTO "dbmaster_navmainmenu" ("id","menu_name","menu_id","icon","position","active") VALUES (1,'Lab','Lab','fa fa-folder-open',1,1);
INSERT INTO "dbmaster_navsubmenu" ("id","sub_menu_name","application_name","url","position","active","navmainmenu_id") VALUES (1,'Cerificate Of Analysis','lab','add&print-coa',1,1,1);
INSERT INTO "dbmaster_navsubmenu" ("id","sub_menu_name","application_name","url","position","active","navmainmenu_id") VALUES (2,'COA list','lab','coa-list',2,1,1);
INSERT INTO "lab_sample" ("id","name") VALUES (1,'EDIBLE GRADE SALT');
INSERT INTO "dbmaster_brand" ("id","name") VALUES (1,'HABARI');
INSERT INTO "dbmaster_brand" ("id","name") VALUES (2,'KAY PREMIUM');
INSERT INTO "dbmaster_brand" ("id","name") VALUES (3,'BAKERY FINE SALT');
INSERT INTO "dbmaster_brand" ("id","name") VALUES (4,'SEMI-CRUSHED');
INSERT INTO "dbmaster_brand" ("id","name") VALUES (5,'DRIED IODIZED COARSE SALT');
INSERT INTO "dbmaster_brand" ("id","name") VALUES (6,'KAY SALT');
INSERT INTO "dbmaster_brand" ("id","name") VALUES (7,'50KG REFINED SALT');
INSERT INTO "dbmaster_brand" ("id","name") VALUES (8,'25KG REFINED SALT');
INSERT INTO "lab_eas" ("id","moisture","chloride","calcium","magnesium","sulphates","alkalinity","insoluble_matter","sieve_size","iodine_max","iodine_min","name") VALUES (1,3,97,0.1,0.1,0.5,0.1,0.2,'85',60,30,'REFINED SALT');
INSERT INTO "lab_eas" ("id","moisture","chloride","calcium","magnesium","sulphates","alkalinity","insoluble_matter","sieve_size","iodine_max","iodine_min","name") VALUES (2,4,96,0.5,0.5,0.5,0.5,1,'N/A',60,30,'COARSE SALT');

