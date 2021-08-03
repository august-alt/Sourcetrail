if (USE_INTERNAL_LIBRARIES)
	add_files(
		EXTERNAL

		catch/catch.hpp
	
		sqlite/CppSQLite3.cpp
		sqlite/CppSQLite3.h

		tinyxml/tinystr.cpp
		tinyxml/tinystr.h
		tinyxml/tinyxml.cpp
		tinyxml/tinyxml.h
		tinyxml/tinyxmlerror.cpp
		tinyxml/tinyxmlparser.cpp
	)

	add_files(
		EXTERNAL_C

		sqlite/sqlite3.c
		sqlite/sqlite3.h
	)
else ()
	add_files(
		EXTERNAL

		sqlite/CppSQLite3.cpp
	        sqlite/CppSQLite3.h
	)
endif ()
