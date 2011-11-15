<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="html" omit-xml-declaration="yes" />
	
	<xsl:param name="UrlBase">.</xsl:param>
	<xsl:param name="ShowAllReportsLink">false</xsl:param>
	
	<xsl:template match="/">
		<html>
		<body>
		<xsl:variable name="SuiteNode" select="//suite" />
		<xsl:if test="count($SuiteNode)>0">
			<xsl:copy-of select="$BarCss" />
			<xsl:for-each select="$SuiteNode">
				<div style="padding:0px 0px 8px 0px">
					<div style="padding:0px 0px 5px 0px">
						<xsl:call-template name="Bar">
							<xsl:with-param name="UrlBase" select="$UrlBase" />
						</xsl:call-template>
					</div>
					<xsl:for-each select="test">
						<div style="padding:5px 0px 0px 34px">
							<xsl:call-template name="SmallBar">
								<xsl:with-param name="UrlBase" select="$UrlBase" />
							</xsl:call-template>
						</div>
					</xsl:for-each>
				</div>
			</xsl:for-each>
			<xsl:if test="$ShowAllReportsLink='true' and $UrlBase!=''">
				<p><a href="{$UrlBase}">All Reports</a></p>
			</xsl:if>
		</xsl:if>
		</body>
		</html>
	</xsl:template>
	
	<xsl:variable name="PassedColor">Green</xsl:variable>
	<xsl:variable name="KnownIssueColor">DarkGoldenrod</xsl:variable>
	<xsl:variable name="FailedColor">Red</xsl:variable>
	<xsl:variable name="NotExecutedColor">Gray</xsl:variable>
	
	<xsl:variable name="BarCss">
		<style>
			.AT-Passed{
				color:<xsl:value-of select="$PassedColor" />;
			}
			.AT-KnownIssues{
				color:<xsl:value-of select="$KnownIssueColor" />;
			}
			.AT-Failed{
				color:<xsl:value-of select="$FailedColor" />;
			}
			.AT-NotExecuted{
				color:<xsl:value-of select="$NotExecutedColor" />;
			}
			.AT-Bar{
				padding:0px;
				margin:0px;
				height:13px;
			}
			.AT-NumberTd{
				text-align:right;
			}
			.AT-LabelTd{
				padding-left:5px;
			}
		</style>
	</xsl:variable>
	
	<xsl:template name="Graph">
		<xsl:param name="Passed" />
		<xsl:param name="KnownIssues" />
		<xsl:param name="Failed" />
		<xsl:param name="NotExecuted" />
		<xsl:param name="Total" />
		
		<div style="height:13px;font-size:10px;margin:3px 0px;">
			<table cellpadding="0" cellspacing="0" class="AT-Bar" style="width:{$Total}px;">
				<tr class="AT-Bar">
					<xsl:if test="count($Passed)>0 and $Passed!='0'">
						<td class="AT-Bar AT-PassedBar" title="{$Passed} passed" style="width:{$Passed}px;background:{$PassedColor};"></td>
					</xsl:if>
					<xsl:if test="count($KnownIssues)>0 and $KnownIssues!='0'">
						<td class="AT-Bar AT-KnownIssuesBar" title="{$KnownIssues} known issues" style="width:{$KnownIssues}px;background:{$KnownIssueColor};"></td>
					</xsl:if>
					<xsl:if test="count($Failed)>0 and $Failed!='0'">
						<td class="AT-Bar AT-FailedBar" title="{$Failed} failed" style="width:{$Failed}px;background:{$FailedColor};"></td>
					</xsl:if>
					<xsl:if test="count($NotExecuted)>0 and $NotExecuted!='0'">
						<td class="AT-Bar AT-NotExecutedBar" title="{$NotExecuted} not executed" style="width:{$NotExecuted}px;background:{$NotExecutedColor};"></td>
					</xsl:if>
				</tr>
			</table>
		</div>
	</xsl:template>
	
	<xsl:template name="SmallBar">
		
		<xsl:param name="UrlBase"></xsl:param>
		
		<xsl:variable name="Name" select="./@name" />
		<xsl:variable name="State" select="./@state" />
		<xsl:variable name="Report" select="./@testResultsReportFile" />
		<xsl:variable name="DetailedReport" select="./@detailedResultsFile" />
		<xsl:variable name="Passed" select="./@Passed" />
		<xsl:variable name="KnownIssues" select="./@KnownIssues" />
		<xsl:variable name="Failed" select="./@Failed" />
		<xsl:variable name="NotExecuted" select="./@NotExecuted" />
		<xsl:variable name="Total" select="./@TotalTestCases" />
		
		<div style="font-weight:bold"><xsl:value-of select="$Name" /></div>
		<table cellpadding="4" cellspacing="0">
			<tr valign="middle">
				<xsl:if test="$UrlBase!=''">
				<xsl:if test="$Report!=''">
					<td nowrap="true">
						<a href="{$UrlBase}/{$Report}">Report</a>
					</td>
					<td nowrap="true">
						<a href="{$UrlBase}/{$DetailedReport}">Detailed report</a>
					</td>
				</xsl:if>
				</xsl:if>
				<td>
					<xsl:call-template name="Graph">
						<xsl:with-param name="Passed" select="$Passed" />
						<xsl:with-param name="KnownIssues" select="$KnownIssues" />
						<xsl:with-param name="Failed" select="$Failed" />
						<xsl:with-param name="NotExecuted" select="$NotExecuted" />
						<xsl:with-param name="Total" select="$Total" />
					</xsl:call-template>
				</td>
				<td>
					<xsl:if test="count($Passed)>0 and $Passed!=0">
						<span style="white-space:nowrap" class="AT-Passed"><xsl:value-of select="$Passed" /> passed </span>/
					</xsl:if>
					<xsl:if test="count($KnownIssues)>0 and $KnownIssues!=0">
						<span style="white-space:nowrap" class="AT-KnownIssues"><xsl:value-of select="$KnownIssues" /> known issues </span>/
					</xsl:if>
					<xsl:if test="count($Failed)>0 and $Failed!=0">
						<span style="white-space:nowrap" class="AT-Failed"><xsl:value-of select="$Failed" /> failed </span>/
					</xsl:if>
					<xsl:if test="count($NotExecuted)>0 and $NotExecuted!=0">
						<span style="white-space:nowrap" class="AT-NotExecuted"><xsl:value-of select="$NotExecuted" /> not executed </span>/
					</xsl:if>
					<xsl:if test="count($Total)>0 and $Total!=0">
						<span style="white-space:nowrap" class="AT-Total"><xsl:value-of select="$Total" /> total </span>
					</xsl:if>
				</td>
			</tr>
		</table>
	</xsl:template>
	
	<xsl:template name="Bar">
		
		<xsl:param name="UrlBase"></xsl:param>
		
		<xsl:variable name="Name" select="./@name" />
		<xsl:variable name="State" select="./@state" />
		<xsl:variable name="Report" select="./@testResultsReportFile" />
		<xsl:variable name="DetailedReport" select="./@detailedResultsFile" />
		<xsl:variable name="Passed" select="./@Passed" />
		<xsl:variable name="KnownIssues" select="./@KnownIssues" />
		<xsl:variable name="Failed" select="./@Failed" />
		<xsl:variable name="NotExecuted" select="./@NotExecuted" />
		<xsl:variable name="Total" select="./@TotalTestCases" />
		<div style="font-weight:bold"><xsl:value-of select="$Name" /></div>
		<xsl:call-template name="Graph">
			<xsl:with-param name="Passed" select="$Passed" />
			<xsl:with-param name="KnownIssues" select="$KnownIssues" />
			<xsl:with-param name="Failed" select="$Failed" />
			<xsl:with-param name="NotExecuted" select="$NotExecuted" />
			<xsl:with-param name="Total" select="$Total" />
		</xsl:call-template>
		<table cellpadding="0" cellspacing="0">
			<xsl:if test="count($Passed)>0">
				<tr class="AT-Passed"><td class="AT-NumberTd"><xsl:value-of select="$Passed" /></td><td class="AT-LabelTd"> passed</td></tr>
			</xsl:if>
			<xsl:if test="count($KnownIssues)>0">
				<tr class="AT-KnownIssues"><td class="AT-NumberTd"><xsl:value-of select="$KnownIssues" /> </td><td class="AT-LabelTd"> known issues</td></tr>
			</xsl:if>
			<xsl:if test="count($Failed)>0">
				<tr class="AT-Failed"><td class="AT-NumberTd"><xsl:value-of select="$Failed" /></td><td class="AT-LabelTd"> failed</td></tr>
			</xsl:if>
			<xsl:if test="count($NotExecuted)>0">
				<tr class="AT-NotExecuted"><td class="AT-NumberTd"><xsl:value-of select="$NotExecuted" /></td><td class="AT-LabelTd"> not executed</td></tr>
			</xsl:if>
			<xsl:if test="count($Total)>0">
				<tr class="AT-Total"><td class="AT-NumberTd"><xsl:value-of select="$Total" /></td><td class="AT-LabelTd"> total</td></tr>
			</xsl:if>
			<xsl:if test="count($Total)=0">
				<tr><td>total cases number is unknown</td></tr>
			</xsl:if>
		</table>
		<xsl:if test="$UrlBase!=''">
		<xsl:if test="$Report!=''">
			<div style="padding-top:3px">
				<a href="{$UrlBase}/{$Report}">Report</a>
				-
				<a href="{$UrlBase}/{$DetailedReport}">Detailed report</a>
			</div>
		</xsl:if>
		</xsl:if>
	</xsl:template>

</xsl:stylesheet>