export interface SanctionEntity {
  id: string;
  caption: string;
  schema: 'Person' | 'Company' | 'LegalEntity' | 'Vessel' | 'Airplane' | string;
  score: number;
  properties: {
    name: string[];
    alias?: string[];
    birthDate?: string[];
    birthPlace?: string[];
    nationality?: string[];
    country?: string[];
    topics?: string[];
    dataset?: string[];
    notes?: string[];
    identifiers?: string[];
    sanctionBody?: string;
    riskLevel?: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'CLEAN';
    legalBasis?: string;
  };
}

export interface ScreenResponse {
  query: string;
  schema: string;
  timestamp: string;
  durationMs: number;
  totalHits: number;
  dataSource: string;
  results: SanctionEntity[];
}

export interface ComplianceAuditRecord {
  verificationId: string;
  sha256Hash: string;
  timestamp: string;
  searchedEntity: string;
  schemaType: string;
  jurisdiction: string;
  complianceOfficer: string;
  status: 'CLEAR' | 'FLAGGED_SANCTION' | 'FLAGGED_PEP' | 'POTENTIAL_MATCH';
  matchCount: number;
  datasetsChecked: number;
  organization: string;
}
