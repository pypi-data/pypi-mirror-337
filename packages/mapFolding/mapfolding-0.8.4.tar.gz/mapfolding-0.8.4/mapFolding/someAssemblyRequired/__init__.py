"""
Code transformation framework for algorithmic optimization.

This package implements a comprehensive framework for programmatically analyzing,
transforming, and generating Python code. It enables sophisticated algorithm optimization
through abstract syntax tree (AST) manipulation, allowing algorithms to be transformed
from a readable, functional implementation into highly-optimized variants tailored for
different execution environments or specific computational tasks.

Core capabilities:
1. AST Pattern Recognition - Precisely identify and match code patterns using composable predicates
2. Algorithm Transformation - Convert functional state-based implementations to primitive operations
3. Dataclass "Shattering" - Decompose complex state objects into primitive components
4. Performance Optimization - Apply domain-specific optimizations for numerical computation
5. Code Generation - Generate specialized implementations with appropriate imports and syntax

The transformation pipeline supports multiple optimization targets, from general-purpose
acceleration to generating highly-specialized variants optimized for specific input parameters.
This multi-level transformation approach allows for both development flexibility and
runtime performance, preserving algorithm readability in the source while enabling
maximum execution speed in production.

These tools were developed for map folding computation optimization but are designed as
general-purpose utilities applicable to a wide range of code transformation scenarios,
particularly for numerically-intensive algorithms that benefit from just-in-time compilation.
"""
from mapFolding.someAssemblyRequired._theTypes import (
	ast_expr_Slice,
	ast_Identifier,
	ImaAnnotationType,
	astClassHasDOTnameNotName,
	astClassHasDOTnameNotNameOptional,
	astClassHasDOTtarget,
	astClassHasDOTvalue,
	astMosDef,
	intORlist_ast_type_paramORstr_orNone,
	intORstr_orNone,
	list_ast_type_paramORstr_orNone,
	str_nameDOTname,
	typeCertified,
	)

from mapFolding.someAssemblyRequired._toolboxPython import (
	importLogicalPath2Callable,
	importPathFilename2Callable,
	NodeChanger,
	NodeTourist,
	parseLogicalPath2astModule,
	parsePathFilename2astModule,
	)

from mapFolding.someAssemblyRequired._toolboxAntecedents import be, ifThis, 又
from mapFolding.someAssemblyRequired._tool_Make import Make
from mapFolding.someAssemblyRequired._tool_Then import Then

from mapFolding.someAssemblyRequired.transformationTools import (
	dictionaryEstimates,
	extractClassDef,
	extractFunctionDef,
	write_astModule,
	Z0Z_executeActionUnlessDescendantMatches,
	Z0Z_inlineThisFunctionWithTheseValues,
	Z0Z_lameFindReplace,
	Z0Z_makeDictionaryReplacementStatements,
	)
