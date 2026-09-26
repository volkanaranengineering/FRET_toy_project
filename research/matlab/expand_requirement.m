function result = expand_requirement(seed, rule, steps, varargin)
%EXPAND_REQUIREMENT Deterministic elementary cellular automaton, R2018b.
% seed: explicit binary row, NOT automatic natural-language encoding.
% rule: Wolfram code 0..255 or one code per transition (changing receivers).
% steps: number of transitions; first output row is the unmodified input.
% 'DecisionStep',Inf: after this transition, retain a narrowing central band.
% 'DecisionHalfWidth',Inf: initial half-width of that band in cells.
% Projection is an imposed design intervention, not inferred understanding.
p = inputParser;
addParameter(p,'DecisionStep',Inf,@(x) isnumeric(x)&&isscalar(x)&&x>=1&& (isinf(x)||x==fix(x)));
addParameter(p,'DecisionHalfWidth',Inf,@(x) isnumeric(x)&&isscalar(x)&&x>=0&& (isinf(x)||x==fix(x)));
parse(p,varargin{:});
validateattributes(seed,{'numeric','logical'},{'vector','nonempty','real','finite'});
assert(all(seed(:)==0 | seed(:)==1),'Seed must contain only 0 and 1.');
validateattributes(steps,{'numeric'},{'scalar','integer','nonnegative','finite'});
validateattributes(rule,{'numeric'},{'vector','nonempty','integer','>=',0,'<=',255,'finite'});
if isscalar(rule), rules = repmat(rule,1,steps); else, rules = rule(:)'; end
assert(numel(rules)==steps,'Provide one rule or exactly steps rule values.');
seed = logical(seed(:)'); n = numel(seed); w = n+2*steps;
X = false(steps+1,w); domain = false(size(X)); removed = false(size(X));
X(1,steps+(1:n)) = seed; domain(1,steps+(1:n)) = true;
center = (w+1)/2; bg = false;
for t=1:steps
    previous = X(t,:);
    left = [bg previous(1:end-1)]; right = [previous(2:end) bg];
    index = 4*double(left)+2*double(previous)+double(right);
    X(t+1,:) = logical(bitget(uint16(rules(t)),index+1));
    % Infinite uniform exterior evolves too, e.g. rule 1 toggles it.
    bg = logical(bitget(uint16(rules(t)),7*double(bg)+1));
    domain(t+1,steps-t+1:steps+n+t) = true;
    if t>=p.Results.DecisionStep
        radius = max(0,p.Results.DecisionHalfWidth-(t-p.Results.DecisionStep));
        retain = abs((1:w)-center)<=radius;
        removed(t+1,:) = domain(t+1,:) & ~retain;
        X(t+1,removed(t+1,:)) = false;
    end
end
result.bits = X;
result.domain = domain; % predeclared growing window, includes zero cells
result.removed = removed;
result.seed = seed; result.rules = rules; result.steps = steps;
result.x = (1:w)-center;
result.options = p.Results;
end
